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
	page_title = "Healthcare FAQ Bot",
	page_icon = ""
)
st.title("Healthcare FAQ ChatBot")
st.write("Hello! How can I help today")

# 2. Read the API key from an environment variable
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
 st.error("GROQ_API_KEY is not configured.")
 st.stop()
client = Groq(api_key=api_key)

# 3. Customer support instructions
system_prompt = """
	You are a healthcare FAQ assistant.
	Provide general information about:
		- Symptoms and common conditions
		- Healthy lifestyle tips
		- Appointment booking guidance
	Rules:
		- Do not give medical diagnoses.
		- Always recommend consulting a doctor for serious issues.
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
# 	1. What are common symptoms of flu?
# 	2. How much water should I drink daily?
# 	3. How do I book an appointment with a doctor?