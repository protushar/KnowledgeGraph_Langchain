"""
Query Engine for Knowledge Graph
Handles graph construction and LLM-based querying
"""

import networkx as nx
from GraphTransformer import graph_documents
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate


class KnowledgeGraphQueryEngine:
    def __init__(self, model="qwen3:1.7b", temperature=0):
        """Initialize the query engine with a knowledge graph and LLM"""
        self.G = nx.DiGraph()
        self.llm = ChatOllama(model=model, temperature=temperature)
        self._build_graph()
        
    def _build_graph(self):
        """Build the knowledge graph from documents"""
        for gdoc in graph_documents:
            for node in gdoc.nodes:
                self.G.add_node(node.id, type=node.type)
            for rel in gdoc.relationships:
                self.G.add_edge(rel.source.id, rel.target.id, relation=rel.type)
    
    def get_graph_context(self):
        """Generate human-readable graph context"""
        nodes_info = [f"{node[0]} (type: {node[1].get('type', 'unknown')})" 
                      for node in self.G.nodes(data=True)]
        edges_info = [f"{edge[0]} -> {edge[1]} (relation: {edge[2].get('relation', 'unknown')})" 
                      for edge in self.G.edges(data=True)]
        
        graph_context = f"""
Knowledge Graph Information:
Nodes ({len(self.G.nodes())}): {', '.join(nodes_info) if nodes_info else 'No nodes found'}
Relationships ({len(self.G.edges())}): {', '.join(edges_info) if edges_info else 'No relationships found'}
"""
        return graph_context
    
    def query(self, question):
        """Execute a query against the knowledge graph"""
        graph_context = self.get_graph_context()
        
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are an expert financial advisor analyzing a knowledge graph.

{context}

Answer the following question based on the knowledge graph:
{question}

Provide a clear, structured response with specific steps and recommendations."""
        )
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({"context": graph_context, "question": question})
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    def get_graph_stats(self):
        """Get statistics about the knowledge graph"""
        return {
            "num_nodes": self.G.number_of_nodes(),
            "num_edges": self.G.number_of_edges(),
            "nodes": [node for node in self.G.nodes()],
            "edges": [(u, v, self.G[u][v].get('relation', 'unknown')) 
                     for u, v in self.G.edges()]
        }
