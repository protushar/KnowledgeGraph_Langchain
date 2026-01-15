import os
from dotenv import load_dotenv
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from Docs import docs

load_dotenv()

# Use OpenAI API (works in cloud and locally)
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

graph_transformer = LLMGraphTransformer(llm=llm)
graph_documents = graph_transformer.convert_to_graph_documents(docs)
