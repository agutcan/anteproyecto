import json
from pathlib import Path

import faiss
import numpy as np


class VectorStore:
    def __init__(self, index_path: str, metadata_path: str):
        self.index_path = Path(index_path)
        self.metadata_path = Path(metadata_path)

        self.index = None
        self.metadata: list[dict] = []

    def build(self, vectors: np.ndarray, metadata: list[dict]) -> None:
        if len(vectors) == 0:
            raise ValueError("No vectors to index")

        dim = vectors.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(vectors)

        self.index = index
        self.metadata = metadata

    def save(self) -> None:
        if self.index is None:
            raise RuntimeError("Index is not initialized")

        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.metadata_path.parent.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, str(self.index_path))
        self.metadata_path.write_text(json.dumps(self.metadata, ensure_ascii=True, indent=2), encoding="utf-8")

    def load(self) -> None:
        if not self.index_path.exists() or not self.metadata_path.exists():
            raise FileNotFoundError("Index or metadata does not exist")

        self.index = faiss.read_index(str(self.index_path))
        self.metadata = json.loads(self.metadata_path.read_text(encoding="utf-8"))

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> list[dict]:
        if self.index is None:
            raise RuntimeError("Index is not loaded")

        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)

        scores, indices = self.index.search(query_vector.astype(np.float32), top_k)

        results: list[dict] = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            item = dict(self.metadata[idx])
            item["score"] = float(score)
            results.append(item)

        return results
