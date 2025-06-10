from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

def create_rag_chain(vectorstore):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a helpful customer service assistant. Use the following context to answer the question.

Context: {context}

Question: {question}

Answer:"""
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt_template}
    )
    return chain
