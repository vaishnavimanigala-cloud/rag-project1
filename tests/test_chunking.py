from core.text_cleaner import clean_text
from core.chunker import chunk_text


def test_clean_text_removes_excess_whitespace():
    text = "Hello\\n\\n   world!\\r\\n\\r\\n"
    cleaned = clean_text(text)
    assert "Hello" in cleaned
    assert "world!" in cleaned
    assert "\\n\\n" not in cleaned


def test_chunk_text_creates_overlapping_chunks():
    text = "This is sentence one. This is sentence two. This is sentence three. This is sentence four. "
    chunks = chunk_text(text, chunk_size=40, overlap=10)
    assert len(chunks) >= 2
    assert all(chunk["text"] for chunk in chunks)
    assert chunks[0]["chunk_id"] != chunks[1]["chunk_id"]
