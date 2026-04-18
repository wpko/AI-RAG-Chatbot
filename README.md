🤖 AI RAG Chatbot (PDF + Conversational UI)

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![LangChain](https://img.shields.io/badge/LangChain-RAG-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-LLM-black)
![FAISS](https://img.shields.io/badge/FAISS-VectorDB-purple)
![AI](https://img.shields.io/badge/AI-Chatbot-yellow)
![Project](https://img.shields.io/badge/Project-Portfolio-blueviolet)
---
A full-stack Retrieval-Augmented Generation (RAG) Chatbot with an interactive Streamlit user interface, allowing users to upload PDF documents and ask context-aware questions in a chat-style experience.

## 🚀 Features

### 🧠 AI Capabilities
- PDF-based Question Answering (RAG)
- Context-aware responses using chat history
- Semantic search with vector embeddings
- Accurate answers using retrieved document context

### 🎨 User Interface (Streamlit)
- 💬 Chat-style UI (like ChatGPT)
- 📄 Upload PDF directly from browser
- ⏳ Real-time processing indicator (spinner)
- ⌨️ Typing animation effect for responses
- 🧹 Clear chat button
- ⚠️ Upload validation (prevents asking before upload)

### ⚡ Backend
- FastAPI REST API
- Modular RAG pipeline using LangChain
- Clean answer post-processing
---
### 🏗️ Tech Stack
| Layer      | Technology           |
| ---------- | -------------------- |
| Frontend   | Streamlit            |
| Backend    | FastAPI              |
| AI Model   | OpenAI (gpt-4o-mini) |
| Framework  | LangChain            |
| Vector DB  | FAISS                |
| Embeddings | OpenAI Embeddings    |
---
### 🖼️ UI Preview (Streamlit)

Main Features:

- Upload PDF → Ask Questions → Get AI Answers
- Chat history maintained during session

👉 (You can add screenshot here later)
---
### 📂 Project Structure
```
AI-RAG-Chatbot/
│
├── api/
│   └── main.py              # FastAPI backend
│
├── dashboard/
│   └── app.py      # Streamlit UI (chat interface)
│
├── rag/
│   └── rag_pipline.py              # RAG logic (LangChain)
│
├── data/                   # Uploaded PDFs
├── .env
├── requirements.txt
└── README.md
```

---

### ⚙️ Installation
```
git clone https://github.com/your-username/AI-RAG-Chatbot.git
cd AI-RAG-Chatbot
pip install -r requirements.txt
```

Create .env file:

```
OPENAI_API_KEY=your_api_key_here
```
---
### ▶️ Run Locally
#### 1️⃣ Start Backend
```
uvicorn api.main:app --reload
```
#### 2️⃣ Start Frontend (Streamlit UI)
```
streamlit run dashboard/app.py
```
---
### 📡 API Endpoints
#### 📄 Upload PDF
```
POST /upload
```
#### 💬 Ask Question
```
POST /ask
```
---
### 🧠 How It Works
User uploads PDF via Streamlit UI
Backend processes document → splits into chunks
Embeddings created using OpenAI
Stored in FAISS vector database
User asks question via chat UI
Relevant chunks retrieved
LLM generates final answer
---
### ✨ Key Highlight (Important for Portfolio)

#### 👉 This project demonstrates:

- End-to-end AI application development
- RAG (Retrieval-Augmented Generation) implementation
- Frontend + Backend integration
- Real-world AI use case (Document QA system)
- API deployment (Render)
---
### 🌐 Live Demo
- Backend API:
https://ai-rag-chatbot-fastapi.onrender.com

(You can deploy Streamlit separately if needed)
---
### 🔮 Future Improvements
- Multi-PDF support
- Persistent vector DB (Chroma / Pinecone)
- User login system
- Chat history database
- Drag & drop UI
- Open-source LLM support
---
### 👨‍💻 Author

Wai Phyo Ko
Junior Python / AI Developer
