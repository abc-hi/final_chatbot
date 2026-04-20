# # Backend

import torch
import pandas as pd
import os
import pickle
import faiss
import requests
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI

# =========================
# DEVICE SETUP
# =========================
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

# =========================
# FASTAPI APP
# =========================
app = FastAPI()

# =========================
# LOAD DATASET
# =========================
df = pd.read_csv("Data/final_AI_data.csv")
print(df.head())

def row_to_text(row):
    return f"""
Skills: {row['Skills']}
Experience: {row['Experience']}
Role: {row['Custom_Role']}
"""

texts = df.apply(row_to_text, axis=1).tolist()

# =========================
# EMBEDDING MODEL
# =========================
model_embed = SentenceTransformer('all-MiniLM-L6-v2', device=device)

# =========================
# LOAD / CREATE EMBEDDINGS
# =========================
if os.path.exists("embeddings.pkl"):
    print("Loading embeddings...")
    with open("embeddings.pkl", "rb") as f:
        embeddings = pickle.load(f)
else:
    print("Creating embeddings...")
    embeddings = model_embed.encode(texts, batch_size=32, show_progress_bar=True)
    with open("embeddings.pkl", "wb") as f:
        pickle.dump(embeddings, f)

# =========================
# FAISS INDEX
# =========================
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# =========================
# RETRIEVER
# =========================
def retrieve(query, k=2):
    query_emb = model_embed.encode([query])
    distances, indices = index.search(query_emb, k)
    return [texts[i] for i in indices[0]]

# =========================
# OLLAMA CALL (FIXED)
# =========================
def ask_llm(prompt):
    try:
        url = "http://127.0.0.1:11434/api/chat"

        payload = {
            "model": "llama3",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a strict career advisor. Always follow format exactly."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }

        response = requests.post(url, json=payload)

        return response.json()["message"]["content"]

    except Exception as e:
        return f"❌ Error connecting to Ollama: {str(e)}"

# =========================
# RAG PIPELINE
# =========================
def rag_pipeline(query):
    retrieved_texts = retrieve(query)
    context = "\n".join(retrieved_texts)

    prompt = f"""
Context:
{context}

Question:
{query}

Give EXACTLY 3 job roles.

STRICT FORMAT:

Role: <role name>
Reason: <one sentence>
Skills: <comma separated skills>

Role: <role name>
Reason: <one sentence>
Skills: <comma separated skills>

Role: <role name>
Reason: <one sentence>
Skills: <comma separated skills>

NO extra text.
"""

    return ask_llm(prompt)

# =========================
# API ENDPOINT
# =========================
@app.get("/chat")
def chat(query: str):
    return {"response": rag_pipeline(query)}