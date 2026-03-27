"""
Cliente para AWS Bedrock Knowledge Base y Chat.
Maneja la comunicación con Bedrock para soporte IA.
"""

import logging
import os
from typing import Optional

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class BedrockClient:
    """Cliente para interactuar con AWS Bedrock y Knowledge Base."""

    def __init__(self):
        """Inicializa el cliente de Bedrock."""
        self.aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.kb_id = os.getenv("BEDROCK_KB_ID")
        self.model_id = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0")
        self.model_candidates = self._build_model_candidates()

        self.bedrock_runtime = boto3.client(
            "bedrock-runtime",
            region_name=self.aws_region,
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
        )

        self.bedrock_agent = boto3.client(
            "bedrock-agent-runtime",
            region_name=self.aws_region,
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
        )

    def _build_model_candidates(self) -> list:
        """Construye lista ordenada de modelos candidatos para fallback."""
        env_candidates = os.getenv("BEDROCK_MODEL_CANDIDATES", "")
        candidates = [self.model_id]

        if env_candidates.strip():
            candidates.extend([item.strip() for item in env_candidates.split(",") if item.strip()])

        # Modelos activos típicos en us-east-1 (inference profile IDs).
        candidates.extend(
            [
                "amazon.nova-lite-v1:0",
                "amazon.nova-micro-v1:0",
                "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
                "us.anthropic.claude-3-5-haiku-20241022-v1:0",
                "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
            ]
        )

        # Si alguien configuró un model ID sin el prefijo regional, añadir su variante us.
        expanded = []
        for candidate in candidates:
            expanded.append(candidate)
            if candidate.startswith("anthropic."):
                expanded.append(f"us.{candidate}")

        # Dedupe conservando orden.
        deduped = []
        seen = set()
        for candidate in expanded:
            if candidate not in seen:
                deduped.append(candidate)
                seen.add(candidate)

        return deduped

    def retrieve_from_kb(self, query: str, max_results: int = 5) -> list:
        """
        Recupera documentos de la Knowledge Base usando retrieval.

        Args:
            query: Pregunta del usuario.
            max_results: Número máximo de resultados.

        Returns:
            Lista de fragmentos recuperados.
        """
        try:
            response = self.bedrock_agent.retrieve(
                knowledgeBaseId=self.kb_id,
                retrievalQuery={"text": query},
                retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": max_results}},
            )

            results = []
            for item in response.get("retrievalResults", []):
                results.append(
                    {
                        "content": item.get("content", {}).get("text", ""),
                        "score": item.get("score", 0),
                        "source": item.get("metadata", {}).get("source", "Unknown"),
                    }
                )
            return results
        except ClientError as e:
            logger.error(f"Error retrieving from KB: {str(e)}")
            return []

    def generate_response(
        self, user_message: str, context: Optional[str] = None, system_prompt: Optional[str] = None
    ) -> dict:
        """
        Genera una respuesta usando Bedrock con RAG de Knowledge Base.

        Args:
            user_message: Mensaje del usuario.
            context: Contexto adicional (fragmentos de KB).
            system_prompt: Prompt del sistema personalizado.

        Returns:
            Diccionario con respuesta, confianza y metadatos.
        """
        try:
            kb_results = []
            # Recuperar contexto de KB si no se proporciona
            if context is None:
                kb_results = self.retrieve_from_kb(user_message)
                if kb_results:
                    context = "\n".join([f"- {item['content']}" for item in kb_results])
                    raw_confidence = sum(item["score"] for item in kb_results) / len(kb_results)
                    confidence = self._normalize_confidence(raw_confidence)
                else:
                    context = ""
                    confidence = 0.0
            else:
                confidence = 0.7  # Confianza por defecto si se proporciona contexto

            # Prompt del sistema por defecto para soporte
            if system_prompt is None:
                system_prompt = """Eres el asistente de soporte de ArenaGG. Responde siempre en español claro y breve.
Solo puedes responder usando la informacion recuperada de la base de conocimiento.
Si la informacion no es suficiente, indicalo y ofrece escalar a soporte humano.
Nunca inventes politicas, precios, estados de cuenta o resultados de torneos.
No solicites datos sensibles innecesarios.
Para casos sensibles (pagos, bloqueos, disputas, premios), deriva a soporte humano."""

            # Construir messages en formato claude
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": f"""Contexto de la base de conocimiento:
{context}

Pregunta del usuario:
{user_message}"""
                        }
                    ],
                }
            ]

            # Llamar a Bedrock (con fallback automático a inference profile)
            response = None
            model_candidates = self.model_candidates

            last_error = None
            for candidate in model_candidates:
                try:
                    response = self.bedrock_runtime.converse(
                        modelId=candidate,
                        system=[{"text": system_prompt}],
                        messages=messages,
                        inferenceConfig={"temperature": 0.5, "maxTokens": 512},
                    )
                    break
                except ClientError as inner_error:
                    last_error = inner_error
                    error_code = inner_error.response.get("Error", {}).get("Code", "")
                    error_message = inner_error.response.get("Error", {}).get("Message", "")

                    # Si falla por throughput legacy/on-demand, probamos el siguiente candidato.
                    if (
                        error_code == "ValidationException"
                        and "on-demand throughput isn\u2019t supported" in error_message
                    ):
                        logger.warning(
                            "Model %s rechazado por on-demand throughput; probando fallback.",
                            candidate,
                        )
                        continue

                    if (
                        error_code == "ResourceNotFoundException"
                        and "Model is marked by provider as Legacy" in error_message
                    ):
                        logger.warning(
                            "Model %s marcado como Legacy/inactivo; probando fallback.",
                            candidate,
                        )
                        continue

                    if (
                        error_code == "ResourceNotFoundException"
                        and "Model use case details have not been submitted" in error_message
                    ):
                        logger.warning(
                            "Model %s requiere formulario de use case (Anthropic); probando fallback.",
                            candidate,
                        )
                        continue

                    raise

            if response is None and last_error is not None:
                raise last_error

            # Extraer respuesta
            assistant_message = response["output"]["message"]["content"][0]["text"]

            # Decidir si escalar a humano
            should_escalate = self._should_escalate(user_message, assistant_message, confidence)

            return {
                "response": assistant_message,
                "confidence": confidence,
                "should_escalate": should_escalate,
                "context_used": len(kb_results) if context else 0,
                "success": True,
            }

        except ClientError as e:
            logger.error(f"Error generating response from Bedrock: {str(e)}")
            return {
                "response": "Lo siento, no pude procesar tu pregunta. Por favor contacta a soporte humano.",
                "confidence": 0.0,
                "should_escalate": True,
                "context_used": 0,
                "success": False,
            }

    def _should_escalate(self, user_message: str, response: str, confidence: float) -> bool:
        """
        Determina si el caso debe escalarse a soporte humano.

        Args:
            user_message: Pregunta del usuario.
            response: Respuesta generada.
            confidence: Nivel de confianza de la respuesta (0-1).

        Returns:
            True si debe escalarse, False en otro caso.
        """
        # Palabras/frases sensibles que escalan de forma automática.
        # Evitamos términos demasiado generales como "cuenta" o "resultado"
        # para no escalar consultas normales de FAQ.
        sensitive_keywords = [
            "pago",
            "cobro",
            "reembolso",
            "factura",
            "bloquearon mi cuenta",
            "cuenta bloqueada",
            "disputa",
            "reclamación",
            "reclamacion",
            "premio no recibido",
            "datos personales",
            "robo de cuenta",
        ]

        user_lower = user_message.lower()
        if any(keyword in user_lower for keyword in sensitive_keywords):
            return True

        # Baja confianza
        if confidence < 0.25:
            return True

        # Si la respuesta indica incertidumbre
        uncertainty_phrases = [
            "no tengo informacion",
            "no estoy seguro",
            "no puedo responder",
            "soporte humano",
        ]
        response_lower = response.lower()
        if any(phrase in response_lower for phrase in uncertainty_phrases):
            return True

        return False

    def _normalize_confidence(self, score: float) -> float:
        """Normaliza la puntuación de retrieval a un rango más interpretable para UI."""
        bounded = max(0.0, min(1.0, score))
        # Los scores de retrieval suelen ser conservadores; esta calibración
        # evita que respuestas útiles se perciban como "muy bajas" en la UI.
        adjusted = 0.35 + 0.65 * (bounded**0.7)
        return max(0.08, min(0.98, adjusted))


# Instancia global del cliente
bedrock_client = BedrockClient()
