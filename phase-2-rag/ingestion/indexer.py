from qdrant_client import QdrantClient                                                                                                                                              
from qdrant_client.models import Distance, VectorParams, PointStruct
import os

class Indexer:
    def __init__(self, collection_name="anthropic_docs", host=None, port=6333):
        host = host or os.getenv("QDRANT_HOST", "localhost")
        client = QdrantClient(host=host, port=port)
        self.client = client
        self.collection_name = collection_name
        # create collection
        if not self.client.collection_exists(collection_name):
          self.client.create_collection(
              collection_name=collection_name,
              vectors_config=VectorParams(size=384, distance=Distance.COSINE)
        )

    
    # chunks is the list[dict] from chunk_document(), vectors is from embedder.embed()
    def upsert(self, chunks: list[dict], vectors: list[list[float]],id_offset: int = 0) -> None:            
        
        # upsert
        self.client.upsert(
            collection_name=self.collection_name,
            points=[PointStruct(id=id_offset+i, vector=vec, payload=chunk) for i, (chunk, vec) in enumerate(zip(chunks, vectors))]
        )

    def query(self):
        search_result = self.client.query_points(
            collection_name=self.collection_name,            
            with_payload=True,
            with_vectors=False,
            limit=5
        ).points

        query_count = self.client.count(
            collection_name=self.collection_name,
            exact=True            
        ).count

        print(search_result)
        print()
        print(query_count)
        


if __name__ == "__main__":
    from chunker import *
    from embedder import Embedder
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "ingestion/test.txt"
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    overlap = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    results = chunk_document(path, size, overlap)
    sentences = [sentence['text'] for sentence in results]    
    embedder = Embedder()
    vecs = embedder.embed(sentences)
    client = Indexer()
    client.upsert(results,vecs)
    client.query()
