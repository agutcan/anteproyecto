from .openai_provider import OpenAIProvider


class MistralProvider(OpenAIProvider):
    def __init__(self, api_key: str, model: str, base_url: str = ""):
        super().__init__(
            api_key=api_key,
            model=model,
            base_url=base_url or "https://api.mistral.ai/v1",
        )
