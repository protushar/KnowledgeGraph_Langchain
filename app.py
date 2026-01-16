"""
Streamlit Web UI for Knowledge Graph Query Engine
"""

import streamlit as st
import sys
import os

# Add utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'utils'))

from QueryEngine import KnowledgeGraphQueryEngine
from ImageGenerator import ImageGenerator, generate_query_visualization_prompts


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
    
    # Choose LLM provider
    llm_provider = st.sidebar.selectbox(
        "Select LLM Provider",
        ["Groq (Free, Recommended)", "Ollama (Local)", "OpenAI (Paid)"],
        help="Choose the LLM to use"
    )
    
    # Map display names to provider codes
    provider_map = {
        "Groq (Free, Recommended)": "groq",
        "Ollama (Local)": "ollama",
        "OpenAI (Paid)": "openai"
    }
    provider = provider_map[llm_provider]
    
    if provider == "groq":
        model_choice = st.sidebar.selectbox(
            "Select Groq Model",
            ["llama-3.1-8b-instant", "llama-3.2-90b-vision-preview"],
            help="Choose the Groq model to use"
        )
        st.sidebar.info("✨ Using Groq - Free, no quota limits, super fast!")
    elif provider == "ollama":
        model_choice = st.sidebar.selectbox(
            "Select Ollama Model",
            ["qwen3:1.7b", "mistral", "neural-chat"],
            help="Requires Ollama installed locally"
        )
    else:  # openai
        model_choice = "gpt-3.5-turbo"
        st.sidebar.warning("⚠️ Using OpenAI - Paid API, watch your quota")
    
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
        # Try to get API key from Streamlit secrets (cloud) or environment (local)
        api_key = None
        
        if provider == "groq":
            try:
                api_key = st.secrets.get("GROQ_API_KEY")
            except:
                api_key = os.getenv("GROQ_API_KEY")
        elif provider == "openai":
            try:
                api_key = st.secrets.get("OPENAI_API_KEY")
            except:
                api_key = os.getenv("OPENAI_API_KEY")
        
        st.session_state.engine = KnowledgeGraphQueryEngine(
            llm_provider=provider,
            model=model_choice,
            temperature=temperature,
            api_key=api_key,
            use_ollama=(provider == "ollama")
        )
    
    # Main content
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.header("📊 Knowledge Graph Analysis")
        
        # Tab-based interface
        tab1, tab2, tab3, tab4 = st.tabs(["Query Interface", "Graph Statistics", "Sample Queries", "Image Generator"])
        
        with tab1:
            st.subheader("Ask Your Question")
            st.markdown("Enter a financial question to query the knowledge graph:")
            
            # Always show text input
            user_query = st.text_area(
                "Your Question:",
                height=120,
                placeholder="Enter your financial question here...",
                label_visibility="collapsed",
                key="custom_query"
            )
            
            # Sample queries dropdown
            sample_queries = [
                "Given salary, liabilities, and timeline, is purchasing Mahindra XUV 7XO by year-end feasible?",
                "Which bank can we take a car loan from with the lowest interest rate?",
                "What are the key factors to consider when planning a vehicle purchase?",
                "How should liabilities affect the decision to purchase a car?"
            ]
            
            selected_sample = st.selectbox(
                "Or quick-insert a sample query:",
                [""] + sample_queries,
                help="Select a pre-defined query to auto-fill the textbox above"
            )
            
            # Auto-fill if sample selected
            if selected_sample:
                user_query = selected_sample
                st.info(f"📌 Pre-loaded: {selected_sample}")
            
            # Execute query
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                execute_btn = st.button("🚀 Execute Query", width='stretch')
            
            if execute_btn and user_query:
                with st.spinner("Processing query... This may take a moment⏳"):
                    response = st.session_state.engine.query(user_query)
                
                st.success("Query executed successfully! ✅")
                
                st.subheader("📋 Response")
                st.markdown(response)
                
                # Export option
                col_export1, col_export2 = st.columns(2)
                with col_export1:
                    if st.button("📋 Copy Response", width='stretch'):
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
                st.dataframe(nodes_df, width='stretch')
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
                st.dataframe(edges_data, width='stretch')
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
        
        with tab4:
            st.subheader("🎨 Image Generator")
            st.markdown("Generate images from text prompts using AI models")
            
            # Image generation mode selector
            gen_mode = st.radio(
                "Select Image Generation Mode:",
                ["Custom Prompt", "Generate from Query Result"],
                horizontal=True
            )
            
            if gen_mode == "Custom Prompt":
                st.markdown("### Generate Image from Custom Prompt")
                
                custom_prompt = st.text_area(
                    "Enter your image description:",
                    height=100,
                    placeholder="E.g., 'A professional financial advisor discussing investment options with a client'",
                    label_visibility="collapsed"
                )
                
                col_gen1, col_gen2 = st.columns([1, 1])
                with col_gen1:
                    quality = st.slider("Speed (inference steps):", 15, 50, 25, step=5, help="Lower = faster but lower quality")
                with col_gen2:
                    guidance = st.slider("Guidance Scale:", 1.0, 20.0, 7.5, step=0.5)
                
                if st.button("🎨 Generate Image", width='stretch'):
                    if custom_prompt:
                        with st.spinner("🎨 Generating image... (first time may take 2-3 minutes to load model)⏳"):
                            try:
                                # Cache image generator in session state to avoid reloading
                                if "img_gen" not in st.session_state:
                                    st.session_state.img_gen = ImageGenerator()
                                
                                image = st.session_state.img_gen.generate_image(
                                    custom_prompt,
                                    num_inference_steps=quality,
                                    guidance_scale=guidance
                                )
                                
                                if image:
                                    st.success("Image generated successfully! ✅")
                                    st.image(image, caption=custom_prompt, width='stretch')
                                else:
                                    st.error("Failed to generate image. Please try again.")
                            
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                    else:
                        st.warning("⚠️ Please enter a prompt before generating.")
            
            else:  # Generate from Query Result
                st.markdown("### Generate Images from Query Result")
                
                query_result_prompt = st.text_area(
                    "Paste your query result:",
                    height=150,
                    placeholder="Paste the financial analysis result here...",
                    label_visibility="collapsed"
                )
                
                if st.button("🎨 Generate Visualization Images", width='stretch'):
                    if query_result_prompt:
                        with st.spinner("🎨 Generating visualization images... (first time may take 2-3 minutes)⏳"):
                            try:
                                # Generate prompts from query result
                                prompts = generate_query_visualization_prompts(query_result_prompt)
                                
                                st.info(f"Generated {len(prompts)} visualization prompts from your query result")
                                
                                # Cache image generator in session state
                                if "img_gen" not in st.session_state:
                                    st.session_state.img_gen = ImageGenerator()
                                
                                img_gen = st.session_state.img_gen
                                
                                for idx, prompt in enumerate(prompts, 1):
                                    st.subheader(f"Visualization {idx}")
                                    st.caption(f"Prompt: {prompt}")
                                    
                                    with st.spinner(f"Generating visualization {idx}/{len(prompts)}..."):
                                        image = img_gen.generate_image(prompt, num_inference_steps=25)
                                        
                                        if image:
                                            st.image(image, width='stretch')
                                        else:
                                            st.warning(f"Could not generate visualization {idx}")
                            
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                    else:
                        st.warning("⚠️ Please paste a query result before generating visualizations.")
    
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
