from fastapi import FastAPI, Header, HTTPException

from app.config import settings
from app.embeddings import EmbeddingService
from app.ingest import build_index
from app.providers.factory import build_provider
from app.rag import RAGService
from app.schemas import ChatRequest, ChatResponse, ReindexResponse
from app.vector_store import VectorStore

app = FastAPI(title="subirEC2 RAG API", version="1.0.0")

_embedding_service = EmbeddingService(settings.embedding_model)
_vector_store = VectorStore(settings.index_path, settings.metadata_path)
_llm_provider = build_provider(settings)
_rag_service = RAGService(settings, _embedding_service, _vector_store, _llm_provider)


def _ensure_loaded() -> None:
    if _vector_store.index is None:
        _vector_store.load()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "provider": settings.llm_provider, "model": settings.llm_model}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    try:
        _ensure_loaded()
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Index not found. Run reindex first.")

    result = _rag_service.ask(payload.question)
    return ChatResponse(**result)


@app.post("/reindex", response_model=ReindexResponse)
def reindex(x_admin_token: str = Header(default="")) -> ReindexResponse:
    if x_admin_token != settings.admin_token:
        raise HTTPException(status_code=401, detail="Invalid admin token")

    result = build_index()
    _vector_store.load()
    return ReindexResponse(**result)
