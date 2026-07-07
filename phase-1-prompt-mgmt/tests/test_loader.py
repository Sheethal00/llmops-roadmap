import pytest

def test_load_latest_version(loader):
    spec = loader.load("ticket_classifier")
    assert spec.version == "2"

def test_load_specific_version(loader):
    spec = loader.load("ticket_classifier",1)
    assert spec.version == "1"

def test_missing_prompt_raises(loader):
    with pytest.raises(FileNotFoundError):        
        loader.load("ticket_classifie")

def test_missing_version_raises(loader):
    with pytest.raises(FileNotFoundError):        
        loader.load("ticket_classifier",3)

def test_list_prompts(loader):
    response = loader.list_prompts()
    assert response == [
                {
                    "name": "ticket_classifier",
                    "versions": ["1", "2"],
                    "latest": "2"
                },                
            ]

def test_prompts_history(loader):
    response = loader.history("ticket_classifier")
    assert [spec.version for spec in response] == ["1","2"]