import pickle
import numpy as np
from openai import OpenAI
import faiss
from pathlib import Path

client = OpenAI()

# Caminho seguro baseado no próprio arquivo
BASE_DIR = Path(__file__).resolve().parent

index_path = BASE_DIR / "vector.index"
texts_path = BASE_DIR / "texts.pkl"

index = None
texts = []

# Carrega o FAISS se existir
if index_path.exists():
    index = faiss.read_index(str(index_path))

# Carrega os textos se existir
if texts_path.exists():
    with open(texts_path, "rb") as f:
        texts = pickle.load(f)


def search(query):

    if index is None or not texts:
        return "RAG não carregado."

    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    vector = np.array([emb.data[0].embedding]).astype("float32")

    D, I = index.search(vector, 2)

    results = []

    for idx in I[0]:
        if idx < len(texts):
            results.append(texts[idx])

    return "\n".join(results)
