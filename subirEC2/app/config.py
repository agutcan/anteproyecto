from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    llm_provider: str = "openai"
    llm_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    llm_base_url: str = ""

    aws_region: str = "us-east-1"
    bedrock_model_id: str = "amazon.nova-lite-v1:0"

    embedding_model: str = "intfloat/multilingual-e5-small"
    top_k: int = 5
    min_confidence: float = 0.30

    data_dir: str = "./data"
    docs_dir: str = "./documents"
    index_path: str = "./data/index.faiss"
    metadata_path: str = "./data/metadata.json"

    system_prompt: str = (
        "Eres un asistente de soporte. Responde solo con el contexto recuperado. "
        "Si falta informacion, dilo y recomienda escalar a soporte humano."
    )
    sensitive_keywords: str = (
        "pago,cobro,reembolso,bloqueo,cuenta bloqueada,disputa,premio,dato personal"
    )
    admin_token: str = "change-me"

    @property
    def sensitive_terms(self) -> list[str]:
        return [item.strip().lower() for item in self.sensitive_keywords.split(",") if item.strip()]

    @property
    def resolved_data_dir(self) -> Path:
        path = Path(self.data_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path


settings = Settings()
