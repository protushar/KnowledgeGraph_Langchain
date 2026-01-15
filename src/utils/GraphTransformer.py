from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_ollama import ChatOllama
from Docs import docs

llm = ChatOllama(model="qwen3:1.7b", temperature=0)

graph_transformer = LLMGraphTransformer(llm=llm)
graph_documents = graph_transformer.convert_to_graph_documents(docs)
