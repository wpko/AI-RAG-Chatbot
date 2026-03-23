import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain

load_dotenv()

def create_rag(pdf_path):
    # 1. Load & Split
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # 2. Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)

    # 3. Model & Tokenizer
    model_id = "google/flan-t5-large"

    # 4. Pipeline (Task name ကို ဖြုတ်ပြီး model_id ကို string အနေနဲ့ပါ ထည့်ပေးလိုက်ပါမယ်)
    # ဒါဆိုရင် အခုနက RuntimeError လည်း မတက်တော့ပါဘူး
    hf_pipe = pipeline(
        task="text2text-generation",
        model="google/flan-t5-large",
        tokenizer="google/flan-t5-large",
        max_new_tokens=200,
        min_new_tokens=50,
        temperature=0.5,
        repetition_penalty = 1.2,
        do_sample=True
    )
    
    # 5. LangChain LLM
    llm = HuggingFacePipeline(pipeline=hf_pipe)
    
    # 6. Prompt
    # rag_pipline.py ထဲမှာ ပြင်ရန်
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
    
    PROMPT = PromptTemplate(template=prompt_template, input_variables=['context','question','chat_history'])
    # 7. QA Chain
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
        combine_docs_chain_kwargs={"prompt": PROMPT}
    )
    
    return qa