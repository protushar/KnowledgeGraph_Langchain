"""
Query Engine for Knowledge Graph
Handles graph construction and LLM-based querying
Supports: Groq (free), Ollama (local), OpenAI (paid)
"""

import os
import networkx as nx
from GraphTransformer import graph_documents


class KnowledgeGraphQueryEngine:
    def __init__(self, llm_provider="groq", model=None, temperature=0, api_key=None, use_ollama=False):
        """
        Initialize the query engine with a knowledge graph and LLM
        
        Args:
            llm_provider: "groq" (free), "openai" (paid), or "ollama" (local)
            model: Model name (auto-selected if None)
            temperature: Response creativity (0-1)
            api_key: API key for the provider
            use_ollama: Force local Ollama usage
        """
        self.G = nx.DiGraph()
        self.temperature = temperature
        self.llm_provider = llm_provider
        
        # Initialize LLM based on provider
        if use_ollama:
            self._init_ollama(model)
        elif llm_provider.lower() == "groq":
            self._init_groq(model, api_key)
        elif llm_provider.lower() == "openai":
            self._init_openai(model, api_key)
        else:
            # Default to Groq (free)
            self._init_groq(model, api_key)
        
        self._build_graph()
    
    def _init_groq(self, model=None, api_key=None):
        """Initialize Groq LLM (free)"""
        try:
            from langchain_groq import ChatGroq
            
            # Use provided model or default to llama-3.1-8b
            actual_model = model or "llama-3.1-8b-instant"
            
            self.llm = ChatGroq(
                model=actual_model,
                temperature=self.temperature,
                api_key=api_key or os.getenv("GROQ_API_KEY")
            )
        except Exception as e:
            print(f"Error initializing Groq with model {model}: {e}. Falling back to Ollama.")
            self._init_ollama(model)
    
    def _init_openai(self, model=None, api_key=None):
        """Initialize OpenAI LLM (paid)"""
        try:
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model=model or "gpt-3.5-turbo",
                temperature=self.temperature,
                api_key=api_key or os.getenv("OPENAI_API_KEY")
            )
        except Exception as e:
            print(f"Error initializing OpenAI: {e}. Falling back to Groq.")
            self._init_groq(model)
    
    def _init_ollama(self, model=None):
        """Initialize local Ollama (free, requires installation)"""
        try:
            from langchain_ollama import ChatOllama
            self.llm = ChatOllama(
                model=model or "qwen3:1.7b",
                temperature=self.temperature
            )
        except Exception as e:
            print(f"Error initializing Ollama: {e}. Falling back to Groq.")
            self._init_groq(model)
        
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
        from langchain_core.prompts import PromptTemplate
        
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
