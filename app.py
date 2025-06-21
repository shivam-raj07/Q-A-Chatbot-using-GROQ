import streamlit as st
from langchain_groq import ChatGroq
# from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatMessagePromptTemplate,ChatPromptTemplate
import os

from dotenv import load_dotenv
load_dotenv()

##Langsmith Tracking
#os.environ["LANGCHAIN_AP_KEY"]=os.getenv("LANGCHAIN_API_KEY")
#os.environ["LANGCHAIN_TRACING_V2"]="true"
#os.environ["LANGCHAIN_PROJECT"]="Simple Q&A Chatbot"

prompt=ChatPromptTemplate.from_messages(
    [
    ("system","You are a helpful assistant. Please response to the user queries"),
    ("user","Question:{question}")
    ]
)

def generate_response(question,api_key,llm,temperature,max_token):
    os.environ["GROQ_API_KEY"]=api_key
    llm=ChatGroq(model=llm,temperature=temperature,max_tokens=max_token)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({'question':question})
    return answer

st.title("Q&A Chatbot")

st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your GROQ api key:",type="password")

temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)
llm=st.sidebar.selectbox("Choose Models",options=["llama3-8b-8192","llama3-70b-8192"])

st.write("Go ahead ask any question")
user_input=st.text_input("You:")

if user_input:
    response=generate_response(user_input,api_key,llm,temperature,max_tokens)
    st.write(response)
else:
    st.write("please provide the query")
