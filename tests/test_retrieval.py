import numpy as np

from core.embeddings import LocalEmbeddingModel
from core.retriever import rank_chunks_by_similarity


def test_rank_chunks_by_similarity():
    embedding_model = LocalEmbeddingModel(fallback_dimension=4)
    query = "cat animal pet"
    chunks = [
        {"text": "A dog is a pet animal."},
        {"text": "A cat is a pet animal."},
        {"text": "This is about cars and roads."},
    ]
    query_vector = embedding_model.encode([query])[0]
    chunk_vectors = embedding_model.encode([c["text"] for c in chunks])
    ranked = rank_chunks_by_similarity(query_vector, chunk_vectors, chunks)
    assert ranked[0]["text"] == "A cat is a pet animal."
    assert ranked[0]["similarity"] >= ranked[1]["similarity"]


def test_cosine_similarity_is_between_zero_and_one_for_normalized_vectors():
    a = np.array([1.0, 0.0])
    b = np.array([1.0, 0.0])
    from core.retriever import cosine_similarity

    score = cosine_similarity(a, b)
    assert 0.0 <= score <= 1.0
    assert abs(score - 1.0) < 1e-9
