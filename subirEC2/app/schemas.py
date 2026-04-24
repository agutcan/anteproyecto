from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    confidence: float
    should_escalate: bool
    sources: list[str]


class ReindexResponse(BaseModel):
    documents_indexed: int
    chunks_indexed: int
