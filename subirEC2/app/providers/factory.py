from app.config import Settings
from .base import LLMProvider
from .bedrock_provider import BedrockProvider
from .mistral_provider import MistralProvider
from .openai_provider import OpenAIProvider
from .together_provider import TogetherProvider


def build_provider(settings: Settings) -> LLMProvider:
    provider = settings.llm_provider.lower().strip()

    if provider == "openai":
        return OpenAIProvider(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
            base_url=settings.llm_base_url,
        )
    if provider == "mistral":
        return MistralProvider(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
            base_url=settings.llm_base_url,
        )
    if provider == "together":
        return TogetherProvider(
            api_key=settings.llm_api_key,
            model=settings.llm_model,
            base_url=settings.llm_base_url,
        )
    if provider == "bedrock":
        return BedrockProvider(
            model_id=settings.bedrock_model_id,
            region=settings.aws_region,
        )

    raise ValueError(f"Unsupported provider: {settings.llm_provider}")
