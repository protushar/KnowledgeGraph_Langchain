# Cloud Deployment Fix

## Problem
Streamlit Cloud installation failed because Ollama is not available in the cloud environment.

## Solution
I've updated your code to:
1. ✅ Remove Ollama dependency from requirements.txt
2. ✅ Add OpenAI API support to QueryEngine.py
3. ✅ Updated app.py to use OpenAI by default on cloud

## Files Updated

### 1. requirements.txt
- Removed: `langchain-ollama==0.1.8` and `ollama==0.1.34`
- Added: `openai>=1.0.0`
- This now works perfectly on Streamlit Cloud

### 2. src/utils/QueryEngine.py
- Now supports both Ollama (local) and OpenAI (cloud)
- Auto-fallback to OpenAI if Ollama not available
- Takes `use_ollama` parameter and `api_key`

### 3. app.py
- Detects if running locally with Ollama
- Checkbox to choose "Use Local Ollama"
- Automatically uses OpenAI API on cloud

## Push Changes to GitHub

```powershell
cd c:\Projects\KnowledgeGraph_Langchain

# Commit changes
git add requirements.txt src/utils/QueryEngine.py app.py
git commit -m "Fix cloud deployment: remove Ollama, add OpenAI support"

# Push to GitHub
git push origin main
```

## Next: Configure Streamlit Cloud

1. Go to https://share.streamlit.io
2. Find your app or create new deployment
3. Go to **App menu** (⋮) → **Settings**
4. Click **Secrets**
5. Add this:
```
OPENAI_API_KEY = sk-your-actual-key
```
6. Click Save

App will auto-redeploy with the fix!

## Local Development (Still Works!)

For local development with Ollama:
```powershell
# Make sure Ollama is running
ollama serve

# In another terminal
cd c:\Projects\KnowledgeGraph_Langchain
.venv\Scripts\activate
streamlit run app.py

# Check the "Use Local Ollama" checkbox in sidebar
```

## Troubleshooting

**Still getting errors?**
1. Hard refresh browser (Ctrl+Shift+R)
2. Clear Streamlit cache: Delete `.streamlit` folder in app repo
3. Check Streamlit dashboard logs
4. Verify API key is correct

**No API key error?**
- You need to add `OPENAI_API_KEY` to Streamlit Secrets
- See "Configure Streamlit Cloud" section above

**Works locally but fails on cloud?**
- Make sure you pushed the updated files to GitHub
- Check requirements.txt is updated
- Verify OpenAI API key is in Secrets

---

That's it! Your app should now deploy successfully on Streamlit Cloud.
