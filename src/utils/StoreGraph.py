import networkx as nx
from GraphTransformer import graph_documents
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

G = nx.DiGraph()

for gdoc in graph_documents:
    for node in gdoc.nodes:
        G.add_node(node.id, type=node.type)
    for rel in gdoc.relationships:
        G.add_edge(rel.source.id, rel.target.id, relation=rel.type)

query = """
Which bank we can take car loan from with the lowest interest rate?
"""

# Prepare graph context
nodes_info = [f"{node[0]} (type: {node[1].get('type', 'unknown')})" for node in G.nodes(data=True)]
edges_info = [f"{edge[0]} -> {edge[1]} (relation: {edge[2].get('relation', 'unknown')})" for edge in G.edges(data=True)]

graph_context = f"""
Knowledge Graph Information:
Nodes: {', '.join(nodes_info) if nodes_info else 'No nodes found'}
Relationships: {', '.join(edges_info) if edges_info else 'No relationships found'}
"""

# Initialize LLM
llm = ChatOllama(model="qwen3:1.7b", temperature=0)

# Create prompt template
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are an expert financial advisor analyzing a knowledge graph.

{context}

Answer the following question based on the knowledge graph:
{question}

Provide a clear, structured response with specific steps and recommendations."""
)

print("\n" + "="*70)
print("EXECUTING QUERY AGAINST KNOWLEDGE GRAPH")
print("="*70)
print(f"\nQuery: {query}")
print("\n" + "-"*70)
print("Processing response from LLM...\n")

try:
    # Create chain and execute
    chain = prompt | llm
    response = chain.invoke({"context": graph_context, "question": query})
    
    print("RESPONSE:")
    print("-"*70)
    print(response.content if hasattr(response, 'content') else response)
    print("-"*70)
    print("="*70 + "\n")
except Exception as e:
    print(f"Error executing query: {e}")
    print("="*70 + "\n")