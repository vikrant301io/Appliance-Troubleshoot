# 🚀 Streamlit Cloud Deployment - Quick Start

## Prerequisites ✅
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- OpenAI API key

## Step-by-Step Deployment

### Step 1: Prepare Your Code for GitHub

1. **Make sure your code is in a Git repository:**
   ```bash
   git status
   ```
   
   If not initialized:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create a GitHub repository:**
   - Go to [github.com](https://github.com) and create a new repository
   - Name it (e.g., `appliance-troubleshoot-agent`)
   - Choose **Public** (for free Streamlit Cloud) or **Private** (for paid plan)

3. **Push your code to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

2. **Create New App:**
   - Click the **"New app"** button (top right)
   
3. **Configure Your App:**
   - **Repository**: Select your GitHub repository from the dropdown
   - **Branch**: Select `main` (or your main branch name)
   - **Main file path**: Type `streamlit_app.py` (or `app/main.py` if you prefer)
   - **App URL**: (Optional) Choose a custom URL or use the default
   
4. **Click "Deploy"**

### Step 3: Add Your OpenAI API Key (CRITICAL!)

1. **Go to App Settings:**
   - After deployment starts, click on your app name
   - Click the **"⚙️" (Settings)** button or three dots menu
   - Select **"Secrets"**

2. **Add the Secret:**
   - Click **"Add new secret"** or edit the secrets file
   - Add this content:
   ```toml
   OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
   ```
   - **Important**: Replace with your actual OpenAI API key
   - Click **"Save"**

3. **Restart the App:**
   - The app will automatically restart when you save secrets
   - Or manually restart from the Settings menu

### Step 4: Verify Deployment

1. **Wait for Build:**
   - The build process takes 1-2 minutes
   - Watch the logs for any errors

2. **Check Your App:**
   - Your app will be live at: `https://YOUR-APP-NAME.streamlit.app`
   - Test it by:
     - Selecting a category
     - Uploading a nameplate image
     - Going through the full flow

## File Structure for Streamlit Cloud

Your repository should have this structure:

```
your-repo/
├── .streamlit/
│   └── config.toml          ✅ Created
├── app/
│   └── main.py             ✅ Your main app
├── components/             ✅ UI components
├── data/                   ✅ Data files
├── requirements.txt        ✅ Dependencies
├── config.py              ✅ Configuration
└── ... (other folders)
```

## Common Issues & Solutions

### ❌ Build Fails
- **Check**: All files are committed to Git
- **Check**: `requirements.txt` has all dependencies
- **Check**: Main file path is correct: `app/main.py`

### ❌ App Won't Start
- **Check**: OPENAI_API_KEY is set in Secrets
- **Check**: No errors in deployment logs
- **Check**: All required folders exist

### ❌ Images Not Loading
- **Check**: Image folders are committed to Git:
  - `nameplates/`
  - `Lights Not Working Images/`
  - `Water Leakage/`
  - `Door Not Sealing Properly/`

### ❌ Module Not Found Errors
- **Check**: `requirements.txt` includes all packages
- **Solution**: Add missing packages to `requirements.txt`

## Environment Variables

Set in Streamlit Cloud → Settings → Secrets:

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | Your OpenAI API key |

## Testing Checklist

After deployment, test:
- [ ] Category selection works
- [ ] Photo upload works
- [ ] Manual entry works
- [ ] Issue listing works
- [ ] Troubleshooting flow works
- [ ] Part ordering works
- [ ] Technician booking works
- [ ] Combined order+booking works

## Next Steps

1. ✅ Test your deployed app thoroughly
2. ✅ Share your app URL with users
3. ✅ Monitor API usage and costs
4. ✅ Update app as needed (auto-deploys on git push)

---

**Need Help?**
- Streamlit Docs: [docs.streamlit.io](https://docs.streamlit.io)
- Streamlit Community: [discuss.streamlit.io](https://discuss.streamlit.io)
- Check deployment logs in Streamlit Cloud dashboard

