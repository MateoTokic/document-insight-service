from typing import List, Tuple
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer
from transformers import pipeline


class RAGService:
    def __init__(self):
        self.embedding_model = None
        self.qa_pipeline = None
        self.index = None
        self.chunks = []

    def load_models(self):
        if self.embedding_model is None:
            self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

        if self.qa_pipeline is None:
            self.qa_pipeline = pipeline(
                task="question-answering",
                model="distilbert-base-cased-distilled-squad"
            )

    def build_index(self, chunks: List[str]) -> None:
        self.load_models()

        if not chunks:
            raise ValueError("No chunks provided for indexing.")

        self.chunks = chunks

        embeddings = self.embedding_model.encode(chunks, convert_to_numpy=True)
        embeddings = np.array(embeddings).astype("float32")

        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def retrieve(self, question: str, top_k: int = 3) -> List[str]:
        self.load_models()

        if self.index is None:
            raise ValueError("FAISS index has not been built yet.")

        question_embedding = self.embedding_model.encode([question], convert_to_numpy=True)
        question_embedding = np.array(question_embedding).astype("float32")

        distances, indices = self.index.search(question_embedding, top_k)

        retrieved_chunks = []
        for idx in indices[0]:
            if 0 <= idx < len(self.chunks):
                retrieved_chunks.append(self.chunks[idx])

        return retrieved_chunks

    def answer_question(self, question: str, top_k: int = 3) -> Tuple[str, List[str]]:
        self.load_models()

        retrieved_chunks = self.retrieve(question, top_k=top_k)
        context = "\n\n".join(retrieved_chunks)

        if not context.strip():
            return "No relevant context found.", []

        result = self.qa_pipeline(question=question, context=context)
        answer = result.get("answer", "").strip()

        if not answer:
            answer = "Could not find an answer in the document."

        return answer, retrieved_chunks