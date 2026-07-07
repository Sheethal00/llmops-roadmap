from unittest.mock import MagicMock
from shared.prompt_manager.diff import compare_versions
import pytest

def test_compare_versions(loader):
    client = MagicMock()
    client.run.return_value = {
                            "category": "Billing",
                            "confidence": 0.95,
                            "reason": "Bill has wrong tax amount"
                        }
    results = compare_versions(loader,client,"ticket_classifier",1,2,{"ticket":"some text"})
    assert isinstance(results, dict)
    assert {"v1", "v2"} <= results.keys()
    required_keys = {
        "version",
        "model",
        "rendered_user",
        "response",
    }
    for version in ("v1", "v2"):
        assert isinstance(results[version], dict)
        assert required_keys <= results[version].keys()

def test_multiple_client_calls(loader):
    client = MagicMock()
    client.run.return_value = "Mocked response"
    compare_versions(loader, client, "ticket_classifier", 1, 2, {"ticket": "text"})                                                                                                 
    assert client.run.call_count == 2

def test_bad_version(loader):
    client = MagicMock()
    client.run.return_value = "Mocked response"
    with pytest.raises(FileNotFoundError):                
        compare_versions(loader, client, "ticket_classifier", 1, 3, {"ticket": "text"})                                                                                                 
    