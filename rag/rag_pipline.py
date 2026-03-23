import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain

load_dotenv()

def create_rag(pdf_path):
    # 1. Load & Split
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    docs = text_splitter.split_documents(documents)

    # 2. Embeddings OpenAI
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs,embeddings)

    #3. LLM (OpenAI)
    llm = ChatOpenAI(
        model = "gpt-4o-mini",
        temperature=0.5
    )
   
    #4. Prompt
    prompt_template = """
    You are a helpful AI assistant.

    Use the provided context to answer the question.

    Context:
    {context}

    Chat History:
    {chat_history}

    Question:
    {question}

    Give a clear and concise answer.
    Only provide the answer.
    """
    
    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=['context','question','chat_history']
    )
    #5. QA Chain
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
        combine_docs_chain_kwargs={"prompt": PROMPT}
    )
    
    return qa