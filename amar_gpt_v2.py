import streamlit as st
import supabase
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.schema import HumanMessage
import os


# initialize supabase
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
db_client = supabase.create_client(supabase_url, supabase_key)   

# os.environ["OPENAI_API_KEY"] = st.secrets["ANYSCALE_API_KEY"]

# loading the fine-tuned model
linkedin_ghost_model = "meta-llama/Llama-2-13b-chat-hf:paramkusham:lVvcocT"
# linkedin_ghost_model = "meta-llama/Llama-2-70b-chat-hf:paramkusham:bIRd6Uf"

llm = ChatOpenAI(model = linkedin_ghost_model ,
                openai_api_base = "https://api.endpoints.anyscale.com/v1",
                openai_api_key = os.getenv("ANYSCALE_API_KEY")
                )


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

if source:
  loader = WebBaseLoader("https://the-ken.com/kaching/ka-ching-your-upi-spends-can-now-make-or-break-your-loan-application/")
  data = loader.load()

  # Split
  
  text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
  all_splits = text_splitter.split_documents(data)

  # Store splits
  from langchain_openai import OpenAIEmbeddings
  from langchain.vectorstores import Chroma
  vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

  # RetrievalQA
  qa_chain = RetrievalQA.from_chain_type(
      llm,
      retriever=vectorstore.as_retriever()
  )


if query:
  st.session_state.submitted = True
  if st.session_state.submitted:
     placeholder.empty() 
  prompt = "Write a LinkedIn post like Amar Srivastava on  " + query
  if source:
     result = qa_chain({"query": prompt})
     post = result['result']
  else:
     post = run_llm(prompt)
  db_client.table("amar_gpt").insert({
        "query": prompt,
        "response": post
    }).execute()
  st.write(post)
