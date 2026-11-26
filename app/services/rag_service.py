import json
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).resolve().parents[2]

POLICY_FILE = BASE_DIR / "knowledge_base" / "airline_policies.json"

class RAGService:
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )

        with open(POLICY_FILE, "r", encoding="utf-8") as f:
            self.documents = json.load(f)

        texts = [
            f"{doc['title']}\n{doc['content']}"
            for doc in self.documents
        ]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    def retrieve(self, query: str, top_k: int = 3):
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            document = self.documents[index]

            results.append({
                "id": document["id"],
                "category": document["category"],
                "title": document["title"],
                "content": document["content"],
                "score": float(score)
            })

        return results


rag_service = RAGService()

if __name__ == "__main__":
    results = rag_service.retrieve("What is the baggage policy?")

    for result in results:
        print(result)