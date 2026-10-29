import os
from groq import Groq
import streamlit as st

os.environ["GROQ_API_KEY"] = "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"
client = Groq(
	api_key = "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"
)

print("Groq connected successfully!!!")

# configure streamlit website
st.set_page_config(
	page_title = "Finance Helper Bot",
	page_icon = ""
)
st.title("Finance Helper ChatBot")
st.write("Hello! How can I help today")

# 2. Read the API key from an environment variable
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
 st.error("GROQ_API_KEY is not configured.")
 st.stop()
client = Groq(api_key=api_key)

# 3. Customer support instructions
system_prompt = """
	You are a finance helper.
	Assist with:
		- Budgeting tips
		- Saving strategies
		- Loan and credit basics
	Rules:
		- Do not give investment advice.
		- Keep answers simple and practical.
"""

# 4. Initialize chat history
if "messages" not in st.session_state:
	st.session_state.messages = []
# 5. Display previous message
for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.write(message["content"])
# 6. Recieve customer questions
question = st.chat_input(
	"Ask about orders, returns, or refunds..."
)

if question:
	st.session_state.messages.append({
		"role": "user",
		"content": question
	})
	with st.chat_message("user"):
		st.write(question)
		messages = [
		 	{"role": "system", "content": system_prompt}
		] + st.session_state.messages

		try:
			with st.chat_message("assistant"):
				with st.spinner("Preparing your answer..."):
					response = client.chat.completions.create(
						model="openai/gpt-oss-120b",
						messages=messages
					)
					answer = response.choices[0].message.content
					st.write(answer)
			st.session_state.messages.append({
				"role": "assistant",
				"content": answer
			})
		except:
			st.error("Unable to generate a response.")
			st.exception(e)
# 7. Clear conversation
if st.button("Clear Chat"):
	st.session_state.messages = []
	st.rerun()

# Sample Questions:
# 	1. How can I save money every month?
# 	2. What is the difference between credit and debit cards?
# 	3. How do personal loans work?