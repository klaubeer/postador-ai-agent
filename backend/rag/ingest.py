import os
import faiss
import pickle
import numpy as np
from openai import OpenAI
 
client = OpenAI()

knowledge_path = "rag"

texts = []

for file in os.listdir(knowledge_path):

    if file.endswith(".txt"):

        with open(f"{knowledge_path}/{file}", "r", encoding="utf-8") as f:
            texts.append(f.read())

embeddings = []

for text in texts:

    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    embeddings.append(emb.data[0].embedding)

dimension = len(embeddings[0])

index = faiss.IndexFlatL2(dimension)

index.add(
    np.array(embeddings).astype("float32")
)

faiss.write_index(index, "rag/vector.index")

with open("rag/texts.pkl", "wb") as f:
    pickle.dump(texts, f)

print("RAG index criado.")
