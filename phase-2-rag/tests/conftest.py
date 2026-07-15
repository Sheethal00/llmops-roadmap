import pytest
from pathlib import Path
from ingestion.embedder import Embedder

@pytest.fixture
def chunker_config():
    config = {                
                "separators" : ["\n\n", "\n", " ", ""],
                "chunk_size" : 10,
                "overlap_size" : 2
            }
    return config

@pytest.fixture
def embedder():
    embedder = Embedder()
    return embedder