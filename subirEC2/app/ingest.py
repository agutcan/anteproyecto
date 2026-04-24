import json

from app.config import settings
from app.embeddings import EmbeddingService
from app.text_utils import chunk_text, read_documents
from app.vector_store import VectorStore


def build_index() -> dict:
    docs = read_documents(settings.docs_dir)

    if not docs:
        raise RuntimeError(f"No documents found in {settings.docs_dir}")

    chunks: list[str] = []
    metadata: list[dict] = []

    for source, text in docs:
        doc_chunks = chunk_text(text, chunk_size=800, overlap=100)
        for idx, chunk in enumerate(doc_chunks):
            chunks.append(f"passage: {chunk}")
            metadata.append(
                {
                    "source": source,
                    "chunk_id": idx,
                    "text": chunk,
                }
            )

    embedding_service = EmbeddingService(settings.embedding_model)
    vectors = embedding_service.encode(chunks)

    store = VectorStore(settings.index_path, settings.metadata_path)
    store.build(vectors=vectors, metadata=metadata)
    store.save()

    return {
        "documents_indexed": len(docs),
        "chunks_indexed": len(chunks),
    }


if __name__ == "__main__":
    result = build_index()
    print(json.dumps(result, ensure_ascii=True))
