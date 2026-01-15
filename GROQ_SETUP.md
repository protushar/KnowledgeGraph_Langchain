# Groq Free LLM Setup Guide

## What is Groq?

✨ **Groq** is a free, lightning-fast AI inference platform with:
- ✅ Completely FREE - No quota limits!
- ✅ Super fast - Fastest LLM inference available
- ✅ No rate limits - Unlimited API calls
- ✅ Cloud-ready - Works perfectly on Streamlit Cloud
- ✅ Open models - Uses Mixtral, Llama, etc.

## Getting Your Groq API Key (2 minutes)

### Step 1: Sign Up
1. Go to https://console.groq.com
2. Sign up with email or Google/GitHub
3. Verify your email

### Step 2: Create API Key
1. Go to https://console.groq.com/keys
2. Click **"Create API Key"**
3. Copy your key (starts with `gsk_`)

### Step 3: Add to Your Project

**Local Development (.env):**
```
GROQ_API_KEY=gsk_your_key_here
```

**Cloud Deployment (Streamlit Secrets):**
1. Go to https://share.streamlit.io
2. Click your app → **Settings** → **Secrets**
3. Add:
```
GROQ_API_KEY = gsk_your_key_here
```
4. Save - App auto-redeploys!

## Available Free Models

Groq offers several free models:

| Model | Speed | Size | Best For |
|-------|-------|------|----------|
| **mixtral-8x7b-32768** | ⚡ Fastest | Large | Default choice |
| **llama2-70b-4096** | ⚡ Fast | Large | Complex tasks |
| **llama-3.1-70b-versatile** | ⚡ Fast | Large | Latest, versatile |
| **gemma-7b-it** | ⚡⚡ Very Fast | Small | Quick responses |

App uses **mixtral-8x7b** by default (best balance).

## How App Uses Groq

The app now supports 3 LLM options:

1. **Groq (Free) ✅ Recommended**
   - No cost, unlimited usage
   - Super fast responses
   - Works everywhere

2. **Ollama (Local, Free)**
   - Download and run on your computer
   - No internet needed
   - Slower than Groq

3. **OpenAI (Paid)**
   - High quality responses
   - Costs money per API call
   - Has quota limits

## Verify It Works

```powershell
cd c:\Projects\KnowledgeGraph_Langchain

# Test locally
.venv\Scripts\activate
streamlit run app.py

# In the app:
# 1. Check "Groq (Free, Recommended)" is selected
# 2. Enter a question
# 3. Click "Execute Query"
# Should get response instantly!
```

## Troubleshooting

### "API key invalid"
- Copy key from https://console.groq.com/keys
- Make sure it starts with `gsk_`
- Check for extra spaces in .env or Secrets

### "RateLimitError"
- Groq free tier has fair usage limits
- Limits reset daily
- For unlimited: Get [Groq Pro](https://console.groq.com/pricing)

### No response
- Check Groq status: https://status.groq.com
- Verify API key is correct
- Check internet connection

## Pricing

**Groq Free Tier:**
- ✅ Unlimited API calls
- ✅ Fair usage policy (typically 100+ calls/min)
- ✅ All models available
- ✅ Perfect for development and demos

**Groq Pro (Optional):**
- Higher rate limits
- Priority support
- Only if you need more than free tier allows

## Compare: Free LLM Options

| Feature | Groq | Ollama | OpenAI |
|---------|------|--------|--------|
| Cost | FREE | FREE | Paid |
| Speed | ⚡⚡⚡ Fast | ⚡ Slow | ⚡⚡ Medium |
| Cloud | ✅ Yes | ❌ No | ✅ Yes |
| Quota | ✅ Unlimited | ✅ Local | ❌ Limited |
| Setup | 2 min | 10 min | 5 min |
| Quality | Good | Good | Excellent |

## Files Updated

- ✅ `requirements.txt` - Added langchain-groq
- ✅ `app.py` - Support for 3 providers
- ✅ `QueryEngine.py` - Smart provider fallback
- ✅ `.env` - Now uses GROQ_API_KEY

## Next Steps

1. **Get Groq API Key** (see Step 1-3 above)
2. **Update .env**: Replace with your Groq key
3. **Test locally**: `streamlit run app.py`
4. **Deploy to cloud**: Push changes and add secret

## Start Using Groq Now!

```bash
# 1. Update .env
GROQ_API_KEY=gsk_your_actual_key

# 2. Run locally
streamlit run app.py

# 3. Select "Groq (Free, Recommended)" in sidebar
# 4. Ask a question and enjoy instant responses! 🚀
```

---

**That's it! You now have free, unlimited LLM access with Groq!** 🎉
