FROM python:3.11-slim

WORKDIR /app

COPY shared/ ./shared/
COPY phase-2-rag/requirements.txt ./phase-2-rag/requirements.txt
RUN pip install --no-cache-dir -r phase-2-rag/requirements.txt

COPY phase-2-rag/ ./phase-2-rag/

ENV PYTHONPATH=/app

WORKDIR /app/phase-2-rag

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
