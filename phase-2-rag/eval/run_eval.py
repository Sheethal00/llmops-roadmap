import sys
from unittest.mock import MagicMock
sys.modules['langchain_community.chat_models.vertexai'] = MagicMock()
import json
from pathlib import Path
from ragas import evaluate, EvaluationDataset
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas.llms import LangchainLLMWrapper
from langchain_anthropic import ChatAnthropic
sys.path.insert(0, str(Path(__file__).parent.parent))
from api.retriever import Retriever
from api.generator import Generator
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_huggingface import HuggingFaceEmbeddings
# from dotenv import load_dotenv
# load_dotenv()

def build_dataset(golden_path):
    golden = json.loads(Path(golden_path).read_text())
    retriever = Retriever()
    generator = Generator()
    
    rows = []
    for item in golden:
        chunks = retriever.retrieve(item["question"], top_k=5)
        answer = generator.generate(item["question"], chunks)
        rows.append({
            "user_input": item["question"],
            "response": answer,
            "retrieved_contexts": [c["text"] for c in chunks],
            "reference": item["ground_truth"],
        })
    return EvaluationDataset.from_list(rows)

if __name__ == "__main__":
    llm = LangchainLLMWrapper(ChatAnthropic(model="claude-sonnet-4-6"))
    dataset = build_dataset("eval/golden_qa.json")
    embedder = LangchainEmbeddingsWrapper(
      HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )
    results = evaluate(dataset,                                                                                                                                                                    
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],                                                                                                
        llm=llm,  
        embeddings=embedder                                                                                                                                                                  
    )                                                                                                                                                                               
    
    from datetime import datetime

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "scores": results.to_pandas()[
            ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]
        ].mean().to_dict(),
    }

    report_path = Path("eval/reports") / f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.write_text(json.dumps(report, indent=2))
    print(f"\nReport saved to {report_path}")

