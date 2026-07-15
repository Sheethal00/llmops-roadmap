import numpy as np

def test_embed_vec_shape(embedder):
    sentences = ["First sentence","Second sentence"]
    vecs = embedder.embed(sentences)    
    assert len(vecs) == 2
    assert len(vecs[0]) == 384 and len(vecs[1]) == 384

def test_embed_norm(embedder):
    sentences = ["First sentence","Second sentence"]
    vecs = embedder.embed(sentences)    
    assert all([abs(np.linalg.norm(vec) - 1.0) < 1e-6 for vec in vecs])