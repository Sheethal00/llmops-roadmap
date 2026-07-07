import pytest
from pathlib import Path
from shared.prompt_manager.loader import PromptLoader

@pytest.fixture
def prompts_dir():
    return Path(__file__).resolve().parents[1] / "prompts"

@pytest.fixture
def loader(prompts_dir):
    return PromptLoader(prompts_dir)