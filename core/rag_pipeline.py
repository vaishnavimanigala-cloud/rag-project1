import numpy as np

from core.chunker import chunk_text
from core.document_loader import extract_document_text
from core.embeddings import LocalEmbeddingModel
from core.model_selector import select_ollama_model
from core.ollama_client import generate_grounded_answer
from core.retriever import rank_chunks_by_similarity
from core.text_cleaner import clean_text


class RAGPipeline:
    def __init__(self, chunk_size=500, overlap=80, top_k=3, min_similarity=0.1, model_name="all-MiniLM-L6-v2"):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.top_k = top_k
        self.min_similarity = min_similarity
        self.embedding_model = LocalEmbeddingModel(model_name=model_name)
        self.indexed_document = None
        self.chunks = []
        self.chunk_vectors = np.empty((0, 0), dtype=float)

    def index_document(self, file_path):
        document = extract_document_text(file_path)
        cleaned_text = clean_text(document["text"])
        if not cleaned_text:
            raise ValueError("The uploaded document is empty or contains no readable text.")

        chunks = chunk_text(
            cleaned_text,
            chunk_size=self.chunk_size,
            overlap=self.overlap,
            source_name=document["source_name"],
        )

        if not chunks:
            raise ValueError("No chunks were created from the uploaded document.")

        chunk_texts = [chunk["text"] for chunk in chunks]
        self.chunk_vectors = self.embedding_model.encode(chunk_texts)
        self.chunks = chunks
        self.indexed_document = document
        return {
            "source_name": document["source_name"],
            "page_count": document["page_count"],
            "char_count": len(cleaned_text),
            "chunk_count": len(chunks),
        }

    def answer_query(self, question, top_k=None, min_similarity=None, model_name=None, temperature=0.2):
        if not self.chunks:
            raise ValueError("Please upload and index a document before asking a question.")

        cleaned_question = clean_text(question)
        if not cleaned_question:
            return {
                "answer": "Please enter a valid question about the uploaded document.",
                "retrieved": [],
                "model": model_name or select_ollama_model(),
            }

        query_vector = self.embedding_model.encode([cleaned_question])[0]
        selected_top_k = self.top_k if top_k is None else top_k
        selected_threshold = self.min_similarity if min_similarity is None else min_similarity

        ranked = rank_chunks_by_similarity(
            query_vector,
            self.chunk_vectors,
            self.chunks,
            top_k=selected_top_k,
            min_score=selected_threshold,
        )

        if not ranked:
            return {
                "answer": "Relevant information was not found in the uploaded document. Please ask a question related to the document content.",
                "retrieved": [],
                "model": model_name or select_ollama_model(),
                "context": "",
            }

        context = "\n\n".join(
            f"[Source: {item['source']} | Page {item.get('page') or 'n/a'} | Chunk {item['chunk_id']}]\n{item['text']}"
            for item in ranked
        )

        chosen_model = model_name or select_ollama_model()
        try:
            answer = generate_grounded_answer(cleaned_question, context, model_name=chosen_model, temperature=temperature)
        except Exception as exc:
            answer = f"I could not generate a grounded answer from the uploaded document. {exc}"

        return {
            "answer": answer,
            "retrieved": ranked,
            "model": chosen_model,
            "context": context,
        }
