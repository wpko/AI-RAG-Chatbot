from pydantic import BaseModel
from rag.rag_pipline import create_rag
from fastapi import FastAPI, UploadFile, File
import shutil
import os

app = FastAPI()

#load RAG pipline
qa_chain = None

class Question(BaseModel):
    question:str
    chat_history:list=[]
    
@app.get('/')
def home():
    return{"message":"AI RAG Chatbot is running"}

@app.post('/upload')
def upload_file(file:UploadFile=File(...)):
    global qa_chain
    print("file received...")
    os.makedirs("data",exist_ok=True)
    file_path = f"data/{file.filename}"
    #save file
    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)
    print("Building RAG...")
    #build RAG
    qa_chain = create_rag(file_path)
    print("RAG created")
    return{"message":"File Uploaded and Processed"}

#Ask API
@app.post('/ask')
def ask_question(data: Question):
    global qa_chain
    #check RAG ready
    if qa_chain is None:
        return{"answer":"Please uploaded a document first."}
    #convert chat_history list to tuple
    chat_history = [
        (item[0],item[1])
        for item in data.chat_history
    ]
    #ask RAG
    response = qa_chain.invoke(
        {
            "question": data.question,
            "chat_history": chat_history
        }
    )
    raw_answer = response.get("answer", "").strip()

    # Cleaning txt
    answer = clean_answer(raw_answer)
    return {
        "answer": answer,
        "raw_debug": raw_answer
    }
    
def clean_answer(raw_answer:str) -> str:
    if not raw_answer:
        return "I don't know based on the document"
    #Remove unwanted prefixes
    if "Answer:" in raw_answer:
        raw_answer = raw_answer.split("Answer:")[-1].strip()
    #Remove repeated context (Just in Case)
    if len(raw_answer)>1000:
        raw_answer = raw_answer[:500] + "..."
    return raw_answer.strip()