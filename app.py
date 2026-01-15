"""
Streamlit Web UI for Knowledge Graph Query Engine
"""

import streamlit as st
import sys
import os

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'utils'))

from QueryEngine import KnowledgeGraphQueryEngine


def main():
    # Page configuration
    st.set_page_config(
        page_title="Knowledge Graph Query Engine",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
        padding: 10px;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.title("🧠 Knowledge Graph Query Engine")
    st.markdown("**Intelligent Financial Analysis using Knowledge Graphs and LLMs**")
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    model_choice = st.sidebar.selectbox(
        "Select LLM Model",
        ["qwen3:1.7b", "mistral", "neural-chat"],
        help="Choose the model to use for analysis"
    )
    
    temperature = st.sidebar.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.1,
        help="Lower = more deterministic, Higher = more creative"
    )
    
    # Initialize session state
    if "engine" not in st.session_state:
        st.session_state.engine = KnowledgeGraphQueryEngine(
            model=model_choice, 
            temperature=temperature
        )
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("📊 Knowledge Graph Analysis")
        
        # Tab-based interface
        tab1, tab2, tab3 = st.tabs(["Query Interface", "Graph Statistics", "Sample Queries"])
        
        with tab1:
            st.subheader("Ask Your Question")
            st.markdown("Enter a financial question to query the knowledge graph:")
            
            # Sample queries
            sample_queries = [
                "Given salary, liabilities, and timeline, is purchasing Mahindra XUV 7XO by year-end feasible?",
                "Which bank can we take a car loan from with the lowest interest rate?",
                "What are the key factors to consider when planning a vehicle purchase?",
                "How should liabilities affect the decision to purchase a car?"
            ]
            
            selected_sample = st.selectbox(
                "Or select a sample query:",
                ["Custom Query"] + sample_queries,
                help="Choose a pre-defined query or enter your own"
            )
            
            if selected_sample == "Custom Query":
                user_query = st.text_area(
                    "Your Question:",
                    height=120,
                    placeholder="Enter your financial question here...",
                    label_visibility="collapsed"
                )
            else:
                user_query = selected_sample
                st.info(f"📌 Selected: {selected_sample}")
            
            # Execute query
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                execute_btn = st.button("🚀 Execute Query", use_container_width=True)
            
            if execute_btn and user_query:
                with st.spinner("Processing query... This may take a moment⏳"):
                    response = st.session_state.engine.query(user_query)
                
                st.success("Query executed successfully! ✅")
                
                st.subheader("📋 Response")
                st.markdown(response)
                
                # Export option
                col_export1, col_export2 = st.columns(2)
                with col_export1:
                    if st.button("📋 Copy Response", use_container_width=True):
                        st.code(response, language="markdown")
            
            elif execute_btn:
                st.warning("⚠️ Please enter a query before executing.")
        
        with tab2:
            st.subheader("Graph Structure")
            
            stats = st.session_state.engine.get_graph_stats()
            
            # Display statistics
            col_stat1, col_stat2 = st.columns(2)
            
            with col_stat1:
                st.metric("Total Nodes", stats["num_nodes"], help="Number of entities in the graph")
            
            with col_stat2:
                st.metric("Total Relationships", stats["num_edges"], help="Number of connections between entities")
            
            # Display nodes
            st.subheader("📌 Nodes in Graph")
            if stats["nodes"]:
                nodes_df = {
                    "Node": stats["nodes"],
                    "Count": [1] * len(stats["nodes"])
                }
                st.dataframe(nodes_df, use_container_width=True)
            else:
                st.info("No nodes found in the graph.")
            
            # Display relationships
            st.subheader("🔗 Relationships in Graph")
            if stats["edges"]:
                edges_data = []
                for source, target, relation in stats["edges"]:
                    edges_data.append({
                        "Source": source,
                        "Relationship": relation,
                        "Target": target
                    })
                st.dataframe(edges_data, use_container_width=True)
            else:
                st.info("No relationships found in the graph.")
        
        with tab3:
            st.subheader("💡 Sample Queries & Use Cases")
            
            st.markdown("""
### Common Financial Analysis Questions:

**1. Vehicle Purchase Feasibility**
- "Given salary, liabilities, and timeline, is purchasing Mahindra XUV 7XO by year-end feasible?"
- "What are the key factors to consider when planning a vehicle purchase?"

**2. Loan Analysis**
- "Which bank can we take a car loan from with the lowest interest rate?"
- "What loan terms are available for car purchases?"

**3. Financial Planning**
- "How should liabilities affect the decision to purchase a car?"
- "What steps should we follow to ensure financial feasibility of a purchase?"

**4. Decision Making**
- "Based on the knowledge graph, what's the best strategy for this financial decision?"
- "What are the risks associated with this purchase plan?"

---

### Tips for Better Results:
✅ Be specific about the financial context (salary, liabilities, timeline)
✅ Ask about specific entities mentioned in the graph (banks, vehicles, timelines)
✅ Request structured responses (steps, recommendations, considerations)
✅ Ask follow-up questions to get more detailed insights
            """)
    
    with col2:
        st.sidebar.markdown("---")
        st.sidebar.header("ℹ️ About")
        st.sidebar.markdown("""
### Knowledge Graph Query Engine

**Purpose:** 
Combine knowledge graphs with LLMs for intelligent financial analysis.

**Technology Stack:**
- 🧠 LangChain + Ollama
- 📊 NetworkX (Graph)
- 🎨 Streamlit (UI)
- 🤖 qwen3:1.7b (LLM)

**How it works:**
1. Documents are transformed into a knowledge graph
2. User submits a financial question
3. LLM analyzes the graph and user question
4. Structured response is generated

**Version:** 1.0.0
        """)
        
        st.sidebar.markdown("---")
        st.sidebar.header("🔧 Troubleshooting")
        
        if st.sidebar.checkbox("Show Debug Info"):
            st.sidebar.subheader("System Information")
            st.sidebar.info(f"""
**Model:** {model_choice}
**Temperature:** {temperature}
**Nodes:** {stats['num_nodes']}
**Edges:** {stats['num_edges']}
            """)


if __name__ == "__main__":
    main()
