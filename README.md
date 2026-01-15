# Knowledge Graph Langchain

A sophisticated Knowledge Graph Query Engine that combines LangChain, NetworkX, and LLMs (via Ollama) for intelligent financial analysis.

## Features

🧠 **Knowledge Graph Processing**
- Automatic document transformation into structured knowledge graphs
- Entity and relationship extraction using LLMs
- Graph visualization and analysis

💬 **Intelligent Query Interface**
- Natural language questions against the knowledge graph
- Context-aware responses using LLM analysis
- Structured financial insights and recommendations

🎨 **Web-based UI**
- Built with Streamlit for easy deployment
- Interactive query interface
- Real-time graph statistics
- Sample queries and use cases

🔧 **Technology Stack**
- **LangChain**: LLM orchestration and RAG
- **Ollama**: Local LLM inference (qwen3:1.7b)
- **NetworkX**: Graph construction and analysis
- **Streamlit**: Web UI framework
- **Python**: Core programming language

## Installation

### Prerequisites
- Python 3.8+
- Ollama (download from https://ollama.ai)
- Git

### Setup Steps

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/KnowledgeGraph_Langchain.git
cd KnowledgeGraph_Langchain
```

2. **Create and activate virtual environment:**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Download Ollama model:**
```bash
ollama pull qwen3:1.7b
```

5. **Set up environment variables:**
Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_key_here  # Optional, only if using OpenAI
```

## Usage

### Run the Streamlit App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Run the Script

```bash
python src/utils/StoreGraph.py
```

## Project Structure

```
KnowledgeGraph_Langchain/
├── app.py                          # Streamlit web application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .env                           # Environment variables (not committed)
├── .gitignore                     # Git ignore rules
└── src/
    └── utils/
        ├── Docs.py               # Document data
        ├── GraphTransformer.py    # Knowledge graph transformation
        ├── StoreGraph.py          # Graph storage and query execution
        └── QueryEngine.py         # Query engine module
```

## Features in Detail

### Knowledge Graph Generation
- Documents are processed and transformed into graph nodes and relationships
- Uses LLM-based extraction for accurate entity and relationship identification
- Supports multiple document formats

### Query Execution
- Natural language questions are processed against the knowledge graph context
- LLM provides structured, actionable insights
- Supports follow-up questions and clarifications

### Financial Analysis
- Loan feasibility analysis
- Purchase decision support
- Financial planning recommendations
- Risk assessment based on graph data

## Configuration

### Model Selection
The app uses `qwen3:1.7b` by default (lightweight, ~1.4GB RAM)

Other available models:
- `mistral` - Faster but requires more RAM (4.4GB)
- `neural-chat` - Balanced option
- `gemma3` - Alternative 3B model

### Temperature Setting
- 0.0 = Deterministic (best for financial analysis)
- 0.5 = Balanced
- 1.0 = Creative (less suitable for financial tasks)

## Deployment

### Streamlit Community Cloud

1. **Push to GitHub:**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Streamlit Cloud:**
   - Visit https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Choose `app.py` as the main file
   - Click "Deploy"

### Local Deployment
```bash
streamlit run app.py --server.port 8501
```

## API Reference

### KnowledgeGraphQueryEngine

```python
from src.utils.QueryEngine import KnowledgeGraphQueryEngine

# Initialize engine
engine = KnowledgeGraphQueryEngine(model="qwen3:1.7b", temperature=0)

# Execute query
response = engine.query("Your financial question here")

# Get graph statistics
stats = engine.get_graph_stats()
```

## Example Queries

- "Given salary, liabilities, and timeline, is purchasing Mahindra XUV 7XO by year-end feasible?"
- "Which bank can we take a car loan from with the lowest interest rate?"
- "What are the key factors to consider when planning a vehicle purchase?"
- "How should liabilities affect the decision to purchase a car?"

## Troubleshooting

### Ollama Model Not Found
```bash
ollama list           # Check installed models
ollama pull qwen3:1.7b  # Download model
```

### Out of Memory Error
- Use a smaller model (`tinyllama` or `phi`)
- Or increase available RAM

### Streamlit Connection Issues
- Ensure Ollama is running: `ollama serve`
- Check firewall settings
- Verify localhost:11434 is accessible

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- Open a GitHub issue
- Check existing documentation
- Review sample queries

## Future Enhancements

- [ ] Multi-document support
- [ ] Custom entity extraction
- [ ] Graph visualization with Pyvis
- [ ] Export to CSV/JSON
- [ ] Query caching
- [ ] Conversation history
- [ ] Multiple LLM support
- [ ] RAG improvements

---

**Built with ❤️ using LangChain, Ollama, and Streamlit**
