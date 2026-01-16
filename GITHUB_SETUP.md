# Quick Start: Push to GitHub & Deploy

## Step 1: Create GitHub Repository

1. Go to **https://github.com/new**
2. Create new repository:
   - **Name:** `KnowledgeGraph_Langchain`
   - **Description:** Knowledge Graph Query Engine with Streamlit
   - **Public** (required for free deployment)
   - **Do NOT initialize** with README, .gitignore, or license
3. Click **"Create repository"**

You'll see commands to push existing code. Copy them.

## Step 2: Push Your Code

Run these commands in PowerShell in your project directory:

```powershell
cd c:\Projects\KnowledgeGraph_Langchain

# Configure git (one time)
git config user.email "your.email@gmail.com"
git config user.name "Your Name"

# Add all files
git add .

# Create commit
git commit -m "Initial commit: Knowledge Graph Query Engine"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/KnowledgeGraph_Langchain.git

# Rename to main if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Deploy on Streamlit Cloud

**IMPORTANT:** Since your app uses Ollama (local LLM), you have two options:

### Option A: Keep Using Ollama (Local Only)
- Run locally: `streamlit run app.py`
- Cannot deploy to Streamlit Cloud
- Perfect for development

### Option B: Switch to OpenAI (Cloud Deployment)
This allows cloud deployment on Streamlit Community Cloud.

#### 3a. Get OpenAI API Key
1. Sign up at https://platform.openai.com
2. Go to https://platform.openai.com/api-keys
3. Create new secret key
4. Copy it (you won't see it again)

#### 3b. Update Files for OpenAI

Modify **src/utils/QueryEngine.py**:

```python
# Replace lines 6-9 with:
import os
from langchain_openai import ChatOpenAI

class KnowledgeGraphQueryEngine:
    def __init__(self, model="gpt-3.5-turbo", temperature=0, api_key=None):
        """Initialize the query engine with a knowledge graph and LLM"""
        self.G = nx.DiGraph()
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model=model, 
            temperature=temperature,
            api_key=self.api_key
        )
        self._build_graph()
```

#### 3c. Update requirements.txt

Replace the content with:
```
langchain==1.2.4
langchain-openai==1.1.7
langchain-experimental==0.4.1
langchain-core==1.2.7
networkx==3.6.1
python-dotenv==1.2.1
streamlit==1.31.1
```

#### 3d. Update app.py

Change line 23:
```python
# From:
st.session_state.engine = KnowledgeGraphQueryEngine(
    model=model_choice, 
    temperature=temperature
)

# To:
st.session_state.engine = KnowledgeGraphQueryEngine(
    model="gpt-3.5-turbo",
    temperature=temperature,
    api_key=st.secrets.get("OPENAI_API_KEY")
)
```

Also update the model selector in sidebar (around line 21):
```python
model_choice = st.selectbox(
    "Select LLM Model",
    ["gpt-3.5-turbo", "gpt-4"],
    help="Choose the model to use for analysis"
)
```

#### 3e. Push Changes
```powershell
git add .
git commit -m "Switch to OpenAI API for cloud deployment"
git push origin main
```

## Step 4: Deploy on Streamlit Community Cloud

1. Go to **https://share.streamlit.io**
2. Click **"New app"** or sign in if needed
3. Fill the form:
   - **GitHub repository:** `YOUR_USERNAME/KnowledgeGraph_Langchain`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy"**
5. Wait for deployment (2-5 minutes)

## Step 5: Add Secrets (If Using OpenAI)

1. In Streamlit dashboard, click your app
2. Go to **"Settings"** (⚙️ icon) → **"Secrets"**
3. Add secret:
   ```
   OPENAI_API_KEY = sk-...your-key-here...
   ```
4. Click **"Save"**
5. App auto-redeploys

## Your App URL

Once deployed: `https://[your-chosen-name].streamlit.app`

## For Local Development (Keep Ollama)

```powershell
# Make sure Ollama is running
ollama serve

# In another terminal
cd c:\Projects\KnowledgeGraph_Langchain
.venv\Scripts\activate
streamlit run app.py
```

## Git Commands Reference

```powershell
# Check status
git status

# See changes
git diff

# View history
git log --oneline

# After making changes
git add .
git commit -m "Your message"
git push origin main
```

---

**Choose your path:**
- 🖥️ **Local:** Keep Ollama, run `streamlit run app.py`
- ☁️ **Cloud:** Use OpenAI, deploy to Streamlit Cloud

Both work great! Just pick what suits your needs.
