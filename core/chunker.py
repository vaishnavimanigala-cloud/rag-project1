import re

from core.text_cleaner import clean_text


def chunk_text(text, chunk_size=500, overlap=80, source_name="document", page_number=None):
    cleaned = clean_text(text)
    if not cleaned:
        return []

    segments = [segment.strip() for segment in re.split(r"(?<=[.!?])\s+|\n{2,}", cleaned) if segment.strip()]
    if not segments:
        return []

    chunks = []
    current = ""
    chunk_index = 1

    for segment in segments:
        candidate = f"{current} {segment}".strip() if current else segment
        if len(candidate) <= chunk_size:
            current = candidate
            continue

        if current:
            chunks.append(
                {
                    "chunk_id": f"chunk_{chunk_index:04d}",
                    "source": source_name,
                    "page": page_number,
                    "text": clean_text(current),
                }
            )
            chunk_index += 1
            overlap_text = current[-overlap:] if overlap and len(current) > overlap else current
            current = f"{overlap_text} {segment}".strip()
        else:
            chunks.append(
                {
                    "chunk_id": f"chunk_{chunk_index:04d}",
                    "source": source_name,
                    "page": page_number,
                    "text": clean_text(segment[:chunk_size]),
                }
            )
            chunk_index += 1
            current = segment[chunk_size - overlap : chunk_size] if overlap and len(segment) > chunk_size else ""

    if current.strip():
        chunks.append(
            {
                "chunk_id": f"chunk_{chunk_index:04d}",
                "source": source_name,
                "page": page_number,
                "text": clean_text(current),
            }
        )

    return chunks
