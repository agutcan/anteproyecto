from app.config import Settings
from app.embeddings import EmbeddingService
from app.providers.base import LLMProvider
from app.vector_store import VectorStore


class RAGService:
    def __init__(
        self,
        settings: Settings,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        llm_provider: LLMProvider,
    ):
        self.settings = settings
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.llm_provider = llm_provider

    def ask(self, question: str) -> dict:
        question = (question or "").strip()
        if not question:
            return {
                "answer": "La pregunta esta vacia.",
                "confidence": 0.0,
                "should_escalate": True,
                "sources": [],
            }

        query_vector = self.embedding_service.encode([f"query: {question}"])
        retrieved = self.vector_store.search(query_vector=query_vector, top_k=self.settings.top_k)

        confidence = max((item.get("score", 0.0) for item in retrieved), default=0.0)
        context = "\n\n".join([item["text"] for item in retrieved])
        sources = list(dict.fromkeys([item["source"] for item in retrieved]))

        should_escalate = self._should_escalate(
            question=question, confidence=confidence, context=context
        )

        if not context:
            answer = (
                "No tengo informacion suficiente en la base de conocimiento para responder con seguridad. "
                "Te recomiendo escalar a soporte humano."
            )
            should_escalate = True
        else:
            answer = self.llm_provider.generate(
                system_prompt=self.settings.system_prompt,
                context=context,
                question=question,
            )

        return {
            "answer": answer,
            "confidence": float(confidence),
            "should_escalate": should_escalate,
            "sources": sources,
        }

    def _should_escalate(self, question: str, confidence: float, context: str) -> bool:
        if confidence < self.settings.min_confidence:
            return True

        text = question.lower()
        if any(term in text for term in self.settings.sensitive_terms):
            return True

        if not context.strip():
            return True

        return False
