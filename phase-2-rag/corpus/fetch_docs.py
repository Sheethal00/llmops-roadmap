import requests
import re
from pathlib import Path

corpus_dir = Path("/home/sheethal/Desktop/LLMOps/llmops-roadmap/phase-2-rag/corpus")
BASE = "https://platform.claude.com/docs/en/"

DOCS = {
      "intro":               "intro.md",
      "context_windows":     "build-with-claude/context-windows.md",
      "extended_thinking":   "build-with-claude/extended-thinking.md",
      "multi_modal":         "build-with-claude/vision.md",
      "tool_use_overview":   "agents-and-tools/tool-use/overview.md",
      "structured_output":   "build-with-claude/structured-outputs.md",
      "prompt_caching":      "build-with-claude/prompt-caching.md"
  }   

def clean(text):
    # 1. Strip ``` fences (and everything between them)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    

    # 2. Strip <Tag ...> ... </Tag> blocks (CodeGroup, Note, Tip, Accordion, etc.)
    text = re.sub(r'<CodeGroup>.*?</CodeGroup>', '', text, flags=re.DOTALL)
    text = re.sub(r'<Note>', '', text, flags=re.DOTALL)
    text = re.sub(r'</Note>', '', text, flags=re.DOTALL)
    text = re.sub(r'<Tip>', '', text, flags=re.DOTALL)
    text = re.sub(r'</Tip>', '', text, flags=re.DOTALL)
    text = re.sub(r'<AccordionGroup>.*?</AccordionGroup>', '', text, flags=re.DOTALL)
    text = re.sub(r'<CardGroup>.*?</CardGroup>', '', text, flags=re.DOTALL)    
    text = re.sub(r'<Accordion title=.*?>', '', text, flags=re.DOTALL)
    text = re.sub(r'<Card .*?>', '', text, flags=re.DOTALL)
    text = re.sub(r'<Tooltip .*?>', '', text, flags=re.DOTALL)

    # 3. Strip bare <Tag> / </Tag> lines
    text = re.sub(r'<[^>]+>', '', text)

    # 4. Normalize multiple blank lines to one
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()
    
for name, path in DOCS.items():
    resp = requests.get(BASE + path)    
    resp.raise_for_status()
    text = resp.text
    (corpus_dir / f"{name}.txt").write_text(clean(text))
    print(f"Saved {name}.txt ({len(text)} chars)")