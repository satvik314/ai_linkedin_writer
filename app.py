import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
load_dotenv()

amar_model = "ft:gpt-3.5-turbo-0613:personal::7tf130i3"

llm = ChatOpenAI(model = amar_model)


def run_llm(prompt):
  messages = [
      HumanMessage(content = prompt)
  ]

  response = llm(messages)
  return response.content


st.title("🤖 Amar GPT")
st.write("🚀 Generate LinkedIn posts on Product like [Amar Srivastava](https://www.linkedin.com/in/amarsrivastava26/)")
st.write("♥️ Powered by GPT-3.5 fine-tuned model.")

query = st.text_input("Please enter the topic")

if query:
  prompt = "Write a LinkedIn post like Amar Srivastava on  " + query
  post = run_llm(prompt)
  st.write(post)

