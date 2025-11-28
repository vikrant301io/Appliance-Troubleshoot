# Push Code to GitHub - Instructions

## GitHub Repository
- **Repository URL**: https://github.com/vikrant301io/Appliance-Troubleshoot.git
- **Your Username**: vikrant301io

## Step-by-Step Instructions

### Option 1: Using PowerShell Script (Recommended)

1. **Open PowerShell** in your project directory:
   ```powershell
   cd C:\Users\ASUS\Desktop\Appliance_Troubleshoot_Agent
   ```

2. **Run the push script**:
   ```powershell
   .\push_to_github.ps1
   ```

3. **When prompted for credentials**:
   - **Username**: `vikrant301io`
   - **Password**: Use a GitHub Personal Access Token (NOT your password)
     - Get token from: https://github.com/settings/tokens
     - Create a token with `repo` permissions

### Option 2: Manual Git Commands

Run these commands one by one in PowerShell:

```powershell
# 1. Initialize Git (if not already done)
git init

# 2. Add remote repository
git remote add origin https://github.com/vikrant301io/Appliance-Troubleshoot.git
# If remote already exists, remove it first:
# git remote remove origin
# git remote add origin https://github.com/vikrant301io/Appliance-Troubleshoot.git

# 3. Stage all files
git add .

# 4. Commit changes
git commit -m "Initial commit: Appliance Troubleshoot Agent with Streamlit Cloud deployment ready"

# 5. Set branch to main
git branch -M main

# 6. Push to GitHub (you'll be prompted for credentials)
git push -u origin main
```

## Important: GitHub Authentication

Since GitHub no longer accepts passwords, you need a **Personal Access Token**:

1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Name it: "Appliance Troubleshoot Agent"
4. Select scope: **`repo`** (full control of private repositories)
5. Click **"Generate token"**
6. **Copy the token** (you won't see it again!)
7. When prompted for password during `git push`, paste the token instead

## What Will Be Pushed

✅ All your app code  
✅ Configuration files  
✅ Data files (except bookings.json which is ignored)  
✅ Image folders  
✅ Streamlit configuration  
✅ Requirements.txt  
✅ All deployment documentation  

❌ Won't be pushed (already in .gitignore):
- `venv/` folder
- `.env` file
- `__pycache__/` folders
- `data/bookings.json`
- Temporary files

## Troubleshooting

### Error: "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/vikrant301io/Appliance-Troubleshoot.git
```

### Error: "Authentication failed"
- Make sure you're using a Personal Access Token, not your password
- Token must have `repo` scope

### Error: "Permission denied"
- Check that you have write access to the repository
- Verify your GitHub username is correct: `vikrant301io`

## After Successful Push

1. ✅ Verify files are on GitHub: https://github.com/vikrant301io/Appliance-Troubleshoot
2. ✅ Check that all folders are there
3. ✅ Proceed to Streamlit Cloud deployment using the guides in:
   - `STREAMLIT_CLOUD_QUICK_START.md`
   - `DEPLOYMENT_STREAMLIT_CLOUD.md`

## Next Steps

After pushing to GitHub:
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Deploy your app using the repository
3. Add your `OPENAI_API_KEY` in Streamlit Cloud Secrets

