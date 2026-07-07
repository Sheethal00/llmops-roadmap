try:
    from .loader import PromptSpec
except ImportError:
    from loader import PromptSpec
from anthropic import Anthropic

class LLMClient:
    def __init__(self, api_key=None):                
        self.api_key = api_key
        self.client = Anthropic(api_key=api_key)
        

    def run(self, spec: PromptSpec, system: str, user: str) -> str:        
        kwargs = dict(
            model=spec.model,
            max_tokens=spec.params.get('max_tokens',1024),            
            messages=[{"role" : "user","content" : user}]
        )
        if system:
            kwargs['system'] = system
        if "temperature" in spec.params:
            kwargs['temperature'] = spec.params.get('temperature')
        
        response = self.client.messages.create(**kwargs)
        return response.content[0].text

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from loader import PromptLoader
    from renderer import render_prompt

    load_dotenv()
    loader = PromptLoader("../../phase-1-prompt-mgmt/prompts/")
    spec = loader.load("ticket_classifier")
    system, user = render_prompt(spec, {"ticket": "My card was charged twice"})
    response = LLMClient().run(spec, system, user)
    print('Response : ',response)
