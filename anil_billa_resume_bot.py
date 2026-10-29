import os
import streamlit as st
from groq import Groq
from langchain_community.document_loaders import PyPDFLoader

# 1. Configure API key
os.environ["GROQ_API_KEY"] = "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"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("Groq connected successfully!!!")

# 2. Configure Streamlit page
st.set_page_config(
    page_title="AnilBilla Resume Bot",
    page_icon="📄"
)
st.title("AnilBilla Resume ChatBot")
st.write("Hello! How can I help today?")

# 3. Load Resume PDF
pdf_path = "AnilBilla_Resume.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()
resume_text = "\n".join([doc.page_content for doc in documents])
print("Pages loaded:", len(documents))

# 4. Build system prompt dynamically from resume
system_prompt = f"""
You are a chatbot that answers questions based on the following resume:

{resume_text}

Rules:
- Answer only from the resume.
- If the answer is not in the resume, say: 'I do not know based on the provided resume.'
"""

# 5. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 7. Receive user question
question = st.chat_input("Ask about AnilBilla, Skill set, or Experience...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

    try:
        with st.chat_message("assistant"):
            with st.spinner("Preparing your answer..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=messages
                )
                answer = response.choices[0].message.content
                st.write(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

    except Exception as e:
        st.error("Unable to generate a response.")
        st.exception(e)

# 8. Clear conversation
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
