import streamlit as st
import requests
import time

# API endpoint
API_URL = "http://127.0.0.1:8000"

# Page config
st.set_page_config(page_title="AI RAG Chatbot", page_icon="🤖")
st.title("🤖 AI RAG Chatbot")

# ✅ Sidebar (Pro UI)
with st.sidebar:
    st.title("⚙️ Settings")
    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ✅ Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
        
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False
    
#Upload PDF
uploaded_file = st.file_uploader("Upload your PDF",type = ["pdf"])
#show warning if no file
if uploaded_file is None:
    st.warning("please upload a document first")

if uploaded_file is not None and not st.session_state.uploaded:
    st.info("Processing document...This may take 10-20 seconds.")
    with st.spinner("Uploading and Processing"):
        try:
            response = requests.post(
                f"{API_URL}/upload",
                files = {"file":uploaded_file.getvalue()},
                timeout=240
            )
            if response.status_code == 200:
                st.success("File Uploaded! You can start asking questions")
                st.session_state.uploaded = True
            else:
                st.error("Upload Failed!!!")
        except Exception as e:
            st.error(f"Error:{str(e)}")
            
# ✅ Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

#disable input until upload
user_input = st.chat_input(
    "Ask a question from your document...",
    disabled=not st.session_state.uploaded
)

#chat logic
if user_input:
    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Show user message
    with st.chat_message("user"):
        st.write(user_input)

    # ✅ Convert chat history for backend
    chat_history = []
    msgs = st.session_state.messages

    for i in range(len(msgs) - 1):
        if msgs[i]["role"] == "user" and msgs[i+1]["role"] == "assistant":
            chat_history.append((
                msgs[i]["content"],      # question
                msgs[i+1]["content"]     # answer
            ))

    # ✅ Call API with loading spinner
    with st.spinner("🤔 Thinking..."):
        try:
            response = requests.post(
                f"{API_URL}/ask",
                json={
                    "question": user_input,
                    "chat_history": chat_history
                },
                timeout=100
            )

            if response.status_code == 200:
                answer = response.json().get("answer", "No answer returned")
            else:
                answer = f"❌ API Error: {response.status_code}"

        except Exception as e:
            answer = f"❌ Connection Error: {str(e)}"

    # ✅ Typing effect (better UX)
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        for word in answer.split():
            full_text += word + " "
            placeholder.write(full_text)
            time.sleep(0.02)

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })