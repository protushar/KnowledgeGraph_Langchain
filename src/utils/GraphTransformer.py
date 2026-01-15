import os
from dotenv import load_dotenv
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from Docs import docs

load_dotenv()

# Use cached graph documents to avoid expensive API calls
# These are pre-computed and updated when needed
from CachedGraphDocuments import graph_documents

# Uncomment below to regenerate graph documents (requires valid OpenAI API key)
# WARNING: This will use API credits and may fail with quota errors
# Uncomment only for local development or when you need to update the graph
"""
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

graph_transformer = LLMGraphTransformer(llm=llm)
graph_documents = graph_transformer.convert_to_graph_documents(docs)
"""
