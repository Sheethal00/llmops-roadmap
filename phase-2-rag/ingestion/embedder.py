from sentence_transformers import SentenceTransformer
  
class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name, device="cpu")
        
    def embed(self, texts):
        return self.model.encode(texts, normalize_embeddings=True).tolist()


if __name__ == "__main__":
    import numpy as np
    embedder = Embedder()      
    sentences = [
        "What is a context window?",
        "How large is Claude's context?",      # related topic, different intent
        "What is a context window in LLMs?",   # near-duplicate
        "How do I make chocolate chip cookies?" # unrelated
    ]   

    vecs = embedder.embed(sentences)  # pass a list — one encode() call, more efficient
    
    def cos_sim(a, b):
        return np.dot(a, b)  # already normalized, so dot == cosine

    print(f"related topics:  {cos_sim(vecs[0], vecs[1]):.3f}")   # expect ~0.2–0.4
    print(f"near-duplicate:  {cos_sim(vecs[0], vecs[2]):.3f}")   # expect ~0.85+
    print(f"unrelated:       {cos_sim(vecs[0], vecs[3]):.3f}")   # expect ~0.0–0.1