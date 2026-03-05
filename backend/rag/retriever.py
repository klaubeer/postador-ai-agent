import pickle
import numpy as np
import faiss
from pathlib import Path
from openai import OpenAI

client = OpenAI()

BASE_DIR = Path(__file__).resolve().parent

index_path = BASE_DIR / "vector.index"
texts_path = BASE_DIR / "texts.pkl"

index = None
texts = []

if index_path.exists():
    index = faiss.read_index(str(index_path))

if texts_path.exists():
    with open(texts_path, "rb") as f:
        texts = pickle.load(f)


def search(query, top_k=5):

    if index is None or not texts:
        return ""

    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    vector = np.array([emb.data[0].embedding]).astype("float32")

    D, I = index.search(vector, top_k)

    results = []
    seen = set()

    for idx in I[0]:
        if idx < len(texts):
            text = texts[idx]

            if text not in seen:
                results.append(text)
                seen.add(text)

    return "\n\n".join(results)
