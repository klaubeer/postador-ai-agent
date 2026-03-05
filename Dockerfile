FROM python:3.11-slim

WORKDIR /app

# Instala deps primeiro (cache layer!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia código
COPY . .

# RAG files persistem via volume, mas copia se local
COPY backend/rag/ backend/rag/

EXPOSE $PORT

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
