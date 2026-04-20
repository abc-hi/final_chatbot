# 🚀 AI Career Assistant (RAG-Based Job Role Recommendation System)

## 📌 Overview
AI-powered chatbot that suggests **job roles based on user skills and experience** using **Retrieval-Augmented Generation (RAG)**.
source:https://www.kaggle.com/datasets/dhruval97/datasetresume/data

The system retrieves relevant profiles from a dataset and uses an LLM to generate **accurate, structured career recommendations**.

---

## 🎯 Problem Statement
Choosing the right career role is difficult for:
- Fresh graduates  
- Career switchers  

Manual job searching often leads to:
- Skill mismatch  
- Confusion  
- Time waste  

---

## 💡 Solution
This system:
- Uses embeddings to understand user input  
- Retrieves similar profiles using FAISS  
- Generates ** job role suggestions** using an LLM  

---

## 🧠 Features
- ✅ AI-based job role recommendations  
- ✅ RAG (Retrieval-Augmented Generation) pipeline  
- ✅ Fast similarity search using FAISS  
- ✅ Structured output (Role, Reason, Skills)  
- ✅ FastAPI backend  
- ✅ Streamlit UI  
- ✅ Embedding caching using pickle  


--------------------------------

#### ⚙️ Tech Stack

### 🔹 Backend
- FastAPI  
- FAISS  
- Sentence Transformers (`all-MiniLM-L6-v2`)  
- Ollama (LLaMA3)

### 🔹 Frontend
- Streamlit  

### 🔹 Other Tools
- Pandas  
- Pickle  

---

## 📦 Installed Libraries

| Package               | Version  |
|----------------------|----------|
| faiss-cpu            | 1.13.2   |
| fastapi              | 0.135.1  |
| ollama               | 0.6.1    |
| pip                  | 26.0.1   |
| ragas                | 0.4.3    |
| sentence-transformers| 5.3.0    |
| streamlit            | 1.55.0   |
| uvicorn              | 0.42.0   |

---

## 🔄 Workflow
1. Load dataset  
2. Convert rows into text format  
3. Generate embeddings  
4. Store embeddings (pickle file)  
5. Create FAISS index  
6. Convert user query to embedding  
7. Retrieve top-k similar results  
8. Send context to LLM  
9. Generate structured response  


## Deployment
backend is deployed on ngrok 
ngrok = exposes your local machine to the internet
Think of ngrok as a temporary tunnel:
-  backend runs on your laptop
- ngrok gives you a public HTTPS URL
- Streamlit Cloud can call your local FastAPI/Ollama through that URL
- When you close ngrok → URL dies
✔ No deployment
✔ No server
✔ No cloud hosting
✔ Just a tunnel to your local machine
This is why you keep two terminals open:
- Terminal 1 → FastAPI
- Terminal 2 → ngrok


⭐ Why ngrok is perfect for your setup
Your architecture is:
- Ollama (local)(ollama is heavy so free versions of renc=der couldnot run it but ngrok can do it)
- Embeddings (local)
- FastAPI (local)
- Streamlit Cloud (remote)
Streamlit Cloud cannot access your laptop directly.
So ngrok acts as the bridge.
Streamlit Cloud → ngrok URL → your laptop → FastAPI → Ollama → RAG
<!--backend url: https://pagan-wildcard-virtual.ngrok-free.dev/chat" to checkon browser backend url:https://pagan-wildcard-virtual.ngrok-free.dev/chat?query=hello"-->


## ▶️ How to Run

Run the project using three terminals:

### 🔹 Terminal 1 – Start Backend (FastAPI)
```bash
# uvicorn rag_app:app --port 8000 --reload
uvicorn rag_app:app --host 0.0.0.0 --port 8000

🔹 Terminal 2 – Start LLM (Ollama)
ollama run llama3
🔹 Terminal 3 – Start Frontend (Streamlit)
# streamlit run streamlit_app.py
ngrok http 8000
backend url:https://pagan-wildcard-virtual.ngrok-free.dev/chat
           