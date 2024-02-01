import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.document_loaders import WebBaseLoader
import os

os.environ["OPENAI_API_KEY"] = st.secrets['OPENAI_API_KEY']

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


loader = WebBaseLoader("https://the-ken.com/kaching/ka-ching-your-upi-spends-can-now-make-or-break-your-loan-application/")
data = loader.load()

# Split
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 50)
all_splits = text_splitter.split_documents(data)

# Store splits
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

# RetrievalQA
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever()
)


question = "Write a post like Amar Srivastava on how UPI transactions trail might soon be used to approve or provide loans!"
result = qa_chain({"query": question})
print(result)
     