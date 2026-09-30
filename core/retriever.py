import numpy as np


def cosine_similarity(vector_a, vector_b):
    a = np.asarray(vector_a, dtype=float).ravel()
    b = np.asarray(vector_b, dtype=float).ravel()
    magnitude = np.linalg.norm(a) * np.linalg.norm(b)
    if magnitude == 0:
        return 0.0
    return float(np.dot(a, b) / magnitude)


def rank_chunks_by_similarity(query_vector, chunk_vectors, chunks, top_k=None, min_score=0.0):
    query_vector = np.asarray(query_vector, dtype=float).ravel()
    chunk_vectors = np.asarray(chunk_vectors, dtype=float)

    ranked = []
    for index, chunk in enumerate(chunks):
        if index >= len(chunk_vectors):
            continue
        score = cosine_similarity(query_vector, chunk_vectors[index])
        if score < min_score:
            continue
        entry = dict(chunk)
        entry["similarity"] = round(float(score), 4)
        ranked.append(entry)

    ranked.sort(key=lambda item: item["similarity"], reverse=True)
    if top_k is not None:
        ranked = ranked[:top_k]
    return ranked
