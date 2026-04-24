import boto3

from .base import LLMProvider


class BedrockProvider(LLMProvider):
    def __init__(self, model_id: str, region: str = "us-east-1"):
        self.model_id = model_id
        self.client = boto3.client("bedrock-runtime", region_name=region)

    def generate(self, system_prompt: str, context: str, question: str) -> str:
        response = self.client.converse(
            modelId=self.model_id,
            system=[{"text": system_prompt}],
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "text": (
                                "Contexto recuperado:\n"
                                f"{context}\n\n"
                                f"Pregunta del usuario:\n{question}"
                            )
                        }
                    ],
                }
            ],
            inferenceConfig={"temperature": 0.2, "maxTokens": 512},
        )
        return response["output"]["message"]["content"][0]["text"].strip()
