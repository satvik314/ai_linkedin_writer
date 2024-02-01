import streamlit as st
import supabase
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os


# initialize supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
db_client = supabase.create_client(supabase_url, supabase_key)   

os.environ["OPENAI_API_KEY"] = st.secrets["ANYSCALE_API_KEY"]

# loading the fine-tuned model
linkedin_ghost_model = "meta-llama/Llama-2-13b-chat-hf:paramkusham:lVvcocT"
# linkedin_ghost_model = "meta-llama/Llama-2-70b-chat-hf:paramkusham:bIRd6Uf"

llm = ChatOpenAI(model = linkedin_ghost_model ,
                openai_api_base = "https://api.endpoints.anyscale.com/v1")


def run_llm(prompt):
  messages = [
      HumanMessage(content = prompt)
  ]

  response = llm(messages)
  return response.content

if "submitted" not in st.session_state:
    st.session_state.submitted = False

st.title("🤖 Amar GPT")
st.write("🚀 Generate LinkedIn posts on Product like [Amar Srivastava](https://www.linkedin.com/in/amarsrivastava26/)")
st.write("♥️ Powered by Meta's Llama-70B fine-tuned model.")

query = st.text_input("Please enter the topic")

placeholder = st.empty()

with placeholder.container():
   st.code("""
            Try:
            Psychology of color in product design
            How Uber uses ML models to drive revenue?
            """, language= None)

source = st.text_input("Add source link") 


if query:
  st.session_state.submitted = True
  if st.session_state.submitted:
     placeholder.empty() 
  prompt = "Write a LinkedIn post like Amar Srivastava on  " + query
  post = run_llm(prompt)
  db_client.table("amar_gpt").insert({
        "query": prompt,
        "response": post
    }).execute()
  st.write(post)
