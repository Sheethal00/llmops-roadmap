from unittest.mock import MagicMock, patch
from api.retriever import Retriever

def test_retrieve_returns_top_k():
    with patch("api.retriever.QdrantClient") as mock_client:
        mock_point = MagicMock()
        mock_point.payload = {"text": "some text", "source": "intro", "chunk_index": 0}
        mock_client.return_value.query_points.return_value.points = [mock_point] * 3

        retriever = Retriever()
        results = retriever.retrieve("What is a context window?", top_k=3)

        assert len(results) == 3
        assert "text" in results[0]
        assert "source" in results[0]

def test_retrieve_empty_results():
    with patch("api.retriever.QdrantClient") as mock_client:
        mock_client.return_value.query_points.return_value.points = []

        retriever = Retriever()
        results = retriever.retrieve("unknown question", top_k=5)

        assert results == []
