from qdrant_client import QdrantClient
from ingestion.embedder import Embedder
import os

class Retriever:
    def __init__(self, collection_name="anthropic_docs", host=None, port=6333):
        host = host or os.getenv("QDRANT_HOST", "localhost")
        client = QdrantClient(host=host, port=port)
        self.client = client
        self.collection_name = collection_name

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        # embed the query, search Qdrant, return list of payload dicts
        embedder = Embedder()
        query = embedder.embed(query)
        results = self.client.query_points(
                self.collection_name, 
                query=query, 
                limit=top_k, 
                with_payload=True
            )
        return [point.payload for point in results.points]

if __name__ == "__main__":
    retriever = Retriever()
    question = "How do I know how that I have reached my context window limit ?"
    results = retriever.retrieve(question)
    print(results)