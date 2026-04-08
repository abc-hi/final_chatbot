# 🚀 AI Career Assistant (RAG-Based Job Role Recommendation System)

## 📌 Overview
AI-powered chatbot that suggests **job roles based on user skills and experience** using **Retrieval-Augmented Generation (RAG)**.

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

## ▶️ How to Run

Run the project using three terminals:

### 🔹 Terminal 1 – Start Backend (FastAPI)
```bash
uvicorn rag_app:app --port 8000 --reload
🔹 Terminal 2 – Start LLM (Ollama)
ollama run llama3
🔹 Terminal 3 – Start Frontend (Streamlit)
streamlit run streamlit_app.py