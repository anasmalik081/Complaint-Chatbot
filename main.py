from fastapi import FastAPI
from api.routes import router as complaint_router
from api.database import init_db
from chatbot.knowledge_base import load_knowledge_base
from chatbot.rag_chain import create_rag_chain
from chatbot.bot_logic import ChatSession

app = FastAPI(title="Complaint Management API")

# Initialize DB tables
init_db()

# Include routes
app.include_router(complaint_router)

chat_session = ChatSession()
rag_chain = None  # Will be set in startup

@app.on_event("startup")
def setup():
    global rag_chain
    from chatbot.knowledge_base import load_knowledge_base
    from chatbot.rag_chain import create_rag_chain
    doc_path = "sample_docs/sample_faqs.pdf"
    vectorstore = load_knowledge_base(doc_path)
    rag_chain = create_rag_chain(vectorstore)

@app.post("/chat")
def chat_with_bot(message: str):
    response = chat_session.handle_input(message, rag_chain)
    return {"response": response}