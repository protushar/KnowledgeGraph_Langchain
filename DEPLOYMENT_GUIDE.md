# GitHub Deployment Guide

Follow these steps to deploy your Knowledge Graph Langchain app on Streamlit Community Cloud.

## Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Create a new repository:
   - **Repository name:** `KnowledgeGraph_Langchain`
   - **Description:** Knowledge Graph Query Engine with Streamlit
   - **Visibility:** Public
   - **Initialize repository:** Do NOT check any boxes
3. Click "Create repository"

## Step 2: Push Code to GitHub

Run these commands in your project directory:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Knowledge Graph Query Engine"

# Add remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/KnowledgeGraph_Langchain.git

# Rename branch to main if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Deploy on Streamlit Community Cloud

### Option A: Direct Deployment (Recommended)

1. Go to https://share.streamlit.io
2. Click **"New app"**
3. Fill in the deployment form:
   - **GitHub repository:** `YOUR_USERNAME/KnowledgeGraph_Langchain`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy"**

### Option B: Connect GitHub Account First

1. Go to https://share.streamlit.io
2. Click **"Sign in with GitHub"**
3. Authorize Streamlit
4. Click **"New app"**
5. Select your repository from the dropdown
6. Choose `main` branch
7. Set main file to `app.py`
8. Click **"Deploy"**

## Step 4: Configuration for Streamlit Cloud

The app uses Ollama locally, which won't work on Streamlit Cloud. You have two options:

### Option 1: Use OpenAI API (Recommended for Cloud)

1. Get an OpenAI API key from https://platform.openai.com/api-keys
2. Add as a Streamlit secret:
   - In app dashboard, go to **Settings** → **Secrets**
   - Add: `OPENAI_API_KEY = your_key_here`
3. Update `QueryEngine.py` to use OpenAI:

```python
from langchain_openai import ChatOpenAI

# Replace this line:
# self.llm = ChatOllama(model=model, temperature=temperature)

# With this:
self.llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=temperature,
    api_key=os.getenv("OPENAI_API_KEY")
)
```

### Option 2: Keep Ollama Local (For Local Deployment Only)

Run locally with: `streamlit run app.py`

## Step 5: Update Requirements (If Using OpenAI)

If using OpenAI, update `requirements.txt`:

```
langchain==1.2.4
langchain-openai==1.1.7
langchain-experimental==0.4.1
langchain-core==1.2.7
networkx==3.6.1
python-dotenv==1.2.1
streamlit==1.31.1
```

## Step 6: Monitor Deployment

1. Your app will deploy automatically
2. Watch the logs in the Streamlit dashboard
3. Once deployed, you'll get a public URL like: `https://your-app-name.streamlit.app`

## Troubleshooting

### Build Fails with "ModuleNotFoundError"
- Ensure all imports are in `requirements.txt`
- Check for relative imports and fix them

### App Crashes on Startup
- Check the logs in Streamlit dashboard
- Verify environment variables are set correctly
- Test locally first with `streamlit run app.py`

### Ollama Not Available
- Streamlit Cloud doesn't have Ollama pre-installed
- Use OpenAI API instead (see Option 1 above)
- Or run locally

### Memory Issues
- Reduce model size or use a lighter model
- Check RAM requirements for chosen LLM

## Useful Commands

```bash
# Check git status
git status

# View commit history
git log

# Make changes after initial deployment
git add .
git commit -m "Your message"
git push origin main

# App auto-redeploys on push!
```

## App URL Structure

Once deployed, your app will be at:
```
https://[your-app-name].streamlit.app
```

You can customize the app name in Streamlit dashboard settings.

## Next Steps

1. ✅ Deploy your app
2. 📊 Test all features in production
3. 📝 Update documentation with public URL
4. 🔄 Set up CI/CD if needed
5. 📢 Share with others!

## Support

For issues:
- Check Streamlit docs: https://docs.streamlit.io
- GitHub Issues: https://github.com/streamlit/streamlit/issues
- Streamlit Forum: https://discuss.streamlit.io

---

**Happy Deploying! 🚀**
