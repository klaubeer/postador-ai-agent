import pickle
import numpy as np
from openai import OpenAI
import os
import faiss
 
client = OpenAI()



index = None

index_path = "rag/vector.index"

if os.path.exists(index_path):
    index = faiss.read_index(index_path)

with open("rag/texts.pkl", "rb") as f:
    texts = pickle.load(f)


def search(query):

    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    vector = np.array([emb.data[0].embedding]).astype("float32")

    D, I = index.search(vector, 2)

    results = []

    for idx in I[0]:
        results.append(texts[idx])

    return "\n".join(results)
