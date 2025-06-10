
# 🤖 Cyfuture Complaint Chatbot

This project is a simple RAG-based chatbot application designed to collect and track customer complaints interactively. It combines a **FastAPI backend** for managing complaint records and a **Streamlit UI** for user interaction. The chatbot also uses **LangChain with Google Gemini embeddings** to provide contextual responses based on a sample knowledge base (PDF).

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git https://github.com/anasmalik081/Complaint-Chatbot.git
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your Gemini API Key

Create a `.env` file in the root of the project and add your key like this:

```
GOOGLE_API_KEY=your_google_generative_ai_api_key
```

You can get the key from: https://makersuite.google.com/app/apikey

---

## 🚀 How to Run the Project

### 1. Start the FastAPI Backend

```bash
uvicorn main:app --reload
```

- This will start the API server at `http://localhost:8000`
- You can test API routes in Swagger UI at: `http://localhost:8000/docs`

---

### 2. Start the Streamlit Chat UI

In a **separate terminal**, run:

```bash
streamlit run streamlit_app/app.py
```

- This will launch the chatbot at: `http://localhost:8501`

---

## ✅ Features

- File complaints step-by-step using natural language
- Auto-generates unique complaint IDs
- Retrieve complaint details by ID
- RAG-based fallback using Gemini + LangChain
- Interactive frontend using Streamlit

---

That’s it — your chatbot is ready! Open Streamlit, start a conversation, and enjoy the flow.