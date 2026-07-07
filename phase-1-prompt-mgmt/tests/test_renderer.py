import pytest
from shared.prompt_manager.renderer import render_prompt
import jinja2

def test_happy_path(loader):
    spec = loader.load("ticket_classifier",1)
    system, user = render_prompt(spec,{"ticket":"some text"})    
    assert "some text" in user

def test_missing_variable_raises(loader):
    spec = loader.load("ticket_classifier",1)
    with pytest.raises(jinja2.UndefinedError):                
        system, user = render_prompt(spec,{})
    
def test_empty_system(loader):
    spec = loader.load("ticket_classifier",1)
    spec.system = ""
    system, user = render_prompt(spec,{"ticket":"some text"})
    assert system == ""