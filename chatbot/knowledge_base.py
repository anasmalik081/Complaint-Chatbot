import os
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def load_documents(doc_path: str):
    if doc_path.endswith(".pdf"):
        loader = PyPDFLoader(doc_path)
    else:
        loader = TextLoader(doc_path)
    documents = loader.load()
    return documents

def create_vector_store(documents):
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

def load_knowledge_base(path: str):
    docs = load_documents(path)
    vs = create_vector_store(docs)
    return vs
