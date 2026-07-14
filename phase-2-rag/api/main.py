from fastapi import FastAPI
from pydantic import BaseModel
from api.retriever import Retriever
from api.generator import Generator

app = FastAPI()
retriever = Retriever()
generator = Generator()

class AskRequest(BaseModel):
    question: str
    top_k: int = 5

class AskResponse(BaseModel):
    answer: str
    sources: list[str]

@app.post("/ask")
def ask(request: AskRequest) -> AskResponse:
    chunks = retriever.retrieve(request.question, top_k=request.top_k)
    answer = generator.generate(request.question, chunks)
    sources = list(dict.fromkeys(c["source"] for c in chunks))  # deduplicated, order preserved
    return AskResponse(answer=answer, sources=sources)

@app.get("/health")
def health():                   
    return {"status": "ok"}