from pydantic import BaseModel
from rag.rag_pipline import create_rag
from fastapi import FastAPI, UploadFile, File
import shutil
import os
import re

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
    if qa_chain is None:
        return{"answer":"Please uploaded a document first."}
    #convert list to tuple
    chat_history = [
        (item[0],item[1])
        for item in data.chat_history
    ]
    response = qa_chain.invoke(
        {
            "question": data.question,
            "chat_history": chat_history
        }
    )
    raw_answer = response.get("answer", "").strip()

    # Model ဆီက ထွက်လာတဲ့ စာသားကို သန့်စင်မယ်
    answer = raw_answer

    # ၁။ တကယ်လို့ Model က မဖြေဘဲ Context ကြီးပဲ ပြန်ပေးနေရင် 
    # (Flan-T5 မှာ ဖြစ်တတ်ပါတယ်)
    if "Answer:" in raw_answer:
        parts = raw_answer.split("Answer:")
        # Answer: ရဲ့ နောက်မှာ စာသားရှိမရှိ စစ်မယ်
        potential_answer = parts[-1].strip()
        
        if potential_answer:
            answer = potential_answer
        else:
            # Answer: ရဲ့နောက်မှာ ဘာမှမရှိရင် Fallback အနေနဲ့
            # Context ထဲက ပထမဆုံး စာကြောင်းအချို့ကို ယူခိုင်းကြည့်မယ် (ယာယီဖြေရှင်းချက်)
            answer = "The document mentions information about AI, but the model couldn't summarize it specifically."

    # ၂။ 'don't know' logic ကို ပိုပြီး တိကျအောင် လုပ်မယ်
    # raw_answer ထဲမှာ 'Answer:' ပဲ ပါပြီး ဘာမှ ဆက်မပါလာရင် result က empty ဖြစ်နေမှာမို့လို့ပါ
    lowered_answer = answer.lower()
    
    # အကယ်၍ answer က အရမ်းတိုနေရင် ဒါမှမဟုတ် 'Answer:' ပဲ ဖြစ်နေရင်
    if not answer:
        answer = "I don't know based on the document."

    return {
        "answer": answer,
        "raw_debug": raw_answer
    }