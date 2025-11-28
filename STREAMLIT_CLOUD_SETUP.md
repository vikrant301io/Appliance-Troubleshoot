# Quick Streamlit Cloud Deployment Guide

## 🚀 Quick Steps to Deploy

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click **"New app"**
3. Fill in:
   - **Repository**: Your GitHub repo
   - **Branch**: `main`
   - **Main file path**: `app/main.py`
4. Click **"Deploy"**

### 3. Add Secrets (CRITICAL!)

1. In your app settings, go to **"Secrets"**
2. Add this:
```toml
OPENAI_API_KEY = "your-actual-openai-api-key"
```

### 4. Wait & Test

- Wait ~2 minutes for build
- Open your app URL
- Test the flow!

## 📝 Important Notes

- ✅ Your app entry point: `app/main.py`
- ✅ Make sure all image folders are committed to Git
- ✅ Never commit `.env` file (it's in `.gitignore`)
- ✅ All dependencies are in `requirements.txt`

## 🔗 Your App URL

After deployment: `https://YOUR-APP-NAME.streamlit.app`

---

For detailed instructions, see `DEPLOYMENT_STREAMLIT_CLOUD.md`

