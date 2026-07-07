try:
    from .loader import PromptSpec
except ImportError:
    from loader import PromptSpec
    
from jinja2 import Environment, StrictUndefined

def render_prompt(spec: PromptSpec, variables: dict) -> tuple[str, str]:
    env = Environment(undefined=StrictUndefined)
    template = env.from_string(spec.system)
    system = template.render(**variables)
    template = env.from_string(spec.template)
    user = template.render(**variables)
    return (system,user)

if __name__ == "__main__":
    from .loader import PromptLoader
    loader = PromptLoader("../../phase-1-prompt-mgmt/prompts/")    
    prompt_spec = loader.load("ticket_classifier")     
    print(render_prompt(prompt_spec,variables={'ticket':"The invoice shows the wrong tax amount."}))