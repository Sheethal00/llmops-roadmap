from pathlib import Path
import sys
try:
    from .chunker import chunk_document
    from .embedder import Embedder
    from .indexer import Indexer
except ImportError:
    from chunker import chunk_document
    from embedder import Embedder
    from indexer import Indexer


def run_pipeline(corpus_dir, collection_name="anthropic_docs", chunk_size=1000, chunk_overlap=150):
    embedder = Embedder()
    indexer = Indexer(collection_name=collection_name)
    total = 0 
    id_offset = 0
    
    for txt_file in sorted(Path(corpus_dir).glob("*.txt")):
        chunks = chunk_document(txt_file, chunk_size, chunk_overlap)
        vectors = embedder.embed([c["text"] for c in chunks])
        indexer.upsert(chunks, vectors, id_offset=id_offset)
        id_offset += len(chunks)
        total += len(chunks)
        print(f"{txt_file.name} → {len(chunks)} chunks")
    
    return total


if __name__ == "__main__":
    corpus_dir = sys.argv[1] if len(sys.argv) > 1 else "corpus"
    chunk_size = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    chunk_overlap = int(sys.argv[3]) if len(sys.argv) > 3 else 150
    total = run_pipeline(corpus_dir,"anthropic_docs",chunk_size,chunk_overlap)
    print(f"Total: {total} chunks indexed")
