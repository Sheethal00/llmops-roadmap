try:
    from .renderer import render_prompt
except ImportError:
    from renderer import render_prompt

def compare_versions(loader, client, name, v1, v2, variables) -> dict:    
    spec_v1 = loader.load(name,v1)
    spec_v2 = loader.load(name,v2)
    system1, user1 = render_prompt(spec_v1,variables=variables)
    system2, user2 = render_prompt(spec_v2,variables=variables)
    response_v1 = client.run(spec_v1,system1,user1)
    response_v2 = client.run(spec_v2,system2,user2)
    results = {
      "name": name,
      "variables": variables,
      "v1": {
          "version": spec_v1.version,
          "model": spec_v1.model,
          "params": spec_v1.params,
          "rendered_user": user1,
          "response": response_v1,
      },
      "v2": {
          "version": spec_v2.version,
          "model": spec_v2.model,
          "params": spec_v2.params,
          "rendered_user": user2,
          "response": response_v2,
      }
    }
    return results


if __name__ == "__main__":    
    import os
    from dotenv import load_dotenv
    from loader import PromptLoader
    from renderer import render_prompt
    from client import LLMClient

    load_dotenv()
    loader = PromptLoader("../../phase-1-prompt-mgmt/prompts/")
    llm_client = LLMClient()
    variables = {'ticket':"I can't log into my account. It says my password is incorrect even after resetting it."}
    print(compare_versions(loader,llm_client,"ticket_classifier",1,2,variables))
    