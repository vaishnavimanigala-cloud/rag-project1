import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer


class LocalEmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2", fallback_dimension=256):
        self.model_name = model_name
        self.fallback_dimension = fallback_dimension
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            from sentence_transformers import SentenceTransformer

            self.model = SentenceTransformer(self.model_name)
        except Exception:
            self.model = None

    def encode(self, texts):
        if isinstance(texts, str):
            texts = [texts]

        if self.model is not None:
            vectors = self.model.encode(list(texts), convert_to_numpy=True, normalize_embeddings=True)
            return np.asarray(vectors, dtype=float)

        vectorizer = HashingVectorizer(n_features=self.fallback_dimension, alternate_sign=False, norm=None)
        matrix = vectorizer.transform(list(texts))
        vectors = matrix.toarray().astype(float)
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        return vectors / norms
