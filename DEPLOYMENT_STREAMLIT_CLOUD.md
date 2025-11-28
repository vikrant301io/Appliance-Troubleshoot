# Deployment Guide for Streamlit Cloud

This guide will help you deploy your Appliance Troubleshoot Assistant app to Streamlit Cloud.

## Prerequisites

1. **GitHub Account**: You need a GitHub account to host your code
2. **Streamlit Cloud Account**: Sign up at [share.streamlit.io](https://share.streamlit.io)
3. **OpenAI API Key**: You'll need your OpenAI API key for the app to work

## Step 1: Prepare Your Repository

### 1.1 Push Your Code to GitHub

1. **Initialize Git repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create a new repository on GitHub**:
   - Go to [github.com](https://github.com) and create a new repository
   - **Important**: Make it **public** if using free Streamlit Cloud, or **private** if you have a paid plan

3. **Push your code**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

### 1.2 Ensure Required Files Are Present

Your repository should have:
- ✅ `app/main.py` - Main application file
- ✅ `requirements.txt` - Python dependencies
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ All your app folders (`app/`, `components/`, `data/`, etc.)

## Step 2: Deploy to Streamlit Cloud

### 2.1 Connect Your Repository

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"** button
4. Fill in the deployment form:
   - **Repository**: Select your repository
   - **Branch**: Select `main` (or your main branch)
   - **Main file path**: Enter `app/main.py`
   - **App URL** (optional): Customize if desired
   - Click **"Deploy!"**

### 2.2 Set Environment Variables (Secrets)

**CRITICAL**: You must set your OpenAI API key as a secret!

1. After clicking "Deploy", go to your app's settings
2. Click on **"Secrets"** tab (or **"⚙️ Settings"** → **"Secrets"**)
3. Add the following secret:

```toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

**Important Notes:**
- Replace `your-openai-api-key-here` with your actual OpenAI API key
- Never commit your API key to GitHub!
- Streamlit Cloud encrypts secrets, so they're safe to store here

## Step 3: Verify Deployment

After deployment:

1. **Wait for build to complete** (usually 1-2 minutes)
2. **Check for errors** in the deployment log
3. **Open your app URL** (format: `https://YOUR-APP-NAME.streamlit.app`)
4. **Test the app**:
   - Select a category
   - Upload a nameplate photo or enter details manually
   - Test the full flow

## Troubleshooting

### App Won't Start

**Error: ModuleNotFoundError**
- Check that all dependencies are in `requirements.txt`
- Make sure the file path in Streamlit Cloud is correct (`app/main.py`)

**Error: OPENAI_API_KEY not found**
- Go to app settings → Secrets
- Ensure `OPENAI_API_KEY` is set correctly
- Restart the app after adding secrets

### Images/Assets Not Loading

- Make sure all image folders are included in your repository:
  - `nameplates/` folder
  - `Lights Not Working Images/`
  - `Water Leakage/`
  - `Door Not Sealing Properly/`
- These folders must be committed to Git

### Build Fails

- Check the deployment logs for specific errors
- Ensure `requirements.txt` has all required packages
- Make sure Python version is compatible (Streamlit Cloud uses Python 3.11)

## File Structure for Streamlit Cloud

```
your-repo/
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── app/
│   └── main.py             # Main app file (entry point)
├── components/
├── data/
├── requirements.txt        # Python dependencies
├── config.py
└── ... (other folders)
```

## Environment Variables Reference

The app uses these environment variables (set in Streamlit Cloud Secrets):

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key for GPT models | ✅ Yes |

## Additional Notes

- **Data Persistence**: Data files (`data/*.json`) are stored in the app's file system but won't persist across deployments
- **File Uploads**: Uploaded images are stored in session state only (temporary)
- **Performance**: First load may take a few seconds while dependencies install
- **Custom Domain**: Paid Streamlit Cloud plans allow custom domains

## Next Steps

1. ✅ Deploy your app following the steps above
2. ✅ Test all features
3. ✅ Share your app URL with users
4. ✅ Monitor usage and API costs

## Support

If you encounter issues:
- Check Streamlit Cloud logs: App settings → Logs
- Review Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
- Check Streamlit Community: [discuss.streamlit.io](https://discuss.streamlit.io)

---

**Your app will be live at**: `https://YOUR-APP-NAME.streamlit.app`

