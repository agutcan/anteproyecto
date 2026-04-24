from pathlib import Path


def read_documents(folder: str) -> list[tuple[str, str]]:
    root = Path(folder)
    if not root.exists():
        return []

    docs: list[tuple[str, str]] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").strip()
        if text:
            docs.append((str(path), text))
    return docs


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks: list[str] = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= text_len:
            break
        start = end - overlap

    return chunks
