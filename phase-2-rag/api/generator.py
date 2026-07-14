import anthropic
from pathlib import Path
from shared.prompt_manager.loader import PromptLoader
from shared.prompt_manager.renderer import render_prompt
from dotenv import load_dotenv
load_dotenv()

class Generator:
    def __init__(self, prompts_dir=None):
        self.client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
        prompts_dir = prompts_dir or Path(__file__).parent.parent / "prompts"
        self.loader = PromptLoader(prompts_dir)
    
    def generate(self, question: str, context_chunks: list[dict]) -> str:
        context = "\n\n".join(
            f"[{i+1}] ({c['source']})\n{c['text']}"
            for i, c in enumerate(context_chunks)
        )
        spec = self.loader.load("rag_answer")
        system, user = render_prompt(spec, {"context": context, "question": question})
        response = self.client.messages.create(
            model=spec.model,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user}]
        )                                                       
        return response.content[0].text

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    generator = Generator()
    question = "What are the limitations of multi modal ?"
    chunks = [{'text':'Cannot identify person','source':'multi_modal','chunk_index':0},{'text':'Claude may hallucinate','source':'multi_model','chunk_index':30}]
    response = generator.generate(question,chunks)
    print(response)