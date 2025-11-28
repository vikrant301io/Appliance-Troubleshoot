# Pull and Push to GitHub - Instructions

## Step-by-Step: Pull from Main First, Then Push

### Quick Method: Use the Script

1. **Open PowerShell** in your project directory:
   ```powershell
   cd C:\Users\ASUS\Desktop\Appliance_Troubleshoot_Agent
   ```

2. **Run the pull and push script**:
   ```powershell
   .\pull_and_push.ps1
   ```

### Manual Method: Run Commands Step by Step

Run these commands one by one in PowerShell:

```powershell
# 1. Initialize Git (if not already done)
git init

# 2. Add remote repository
git remote add origin https://github.com/vikrant301io/Appliance-Troubleshoot.git
# If remote already exists, update it:
# git remote set-url origin https://github.com/vikrant301io/Appliance-Troubleshoot.git

# 3. Set branch to main
git branch -M main

# 4. Fetch from remote
git fetch origin main

# 5. Pull from main branch (this will get any existing files)
git pull origin main --allow-unrelated-histories
# Note: --allow-unrelated-histories allows pulling even if histories differ

# 6. Stage all your local files
git add .

# 7. Commit changes
git commit -m "Update: Appliance Troubleshoot Agent with Streamlit Cloud deployment ready"

# 8. Push to GitHub
git push -u origin main
```

## What Happens

1. **Fetch**: Downloads information about the remote repository
2. **Pull**: Merges any existing files from GitHub into your local repository
3. **Add**: Stages all your local files
4. **Commit**: Creates a commit with your changes
5. **Push**: Uploads your code to GitHub

## Handling Conflicts

If there are conflicts during pull:

1. Git will show which files have conflicts
2. Open the conflicted files and resolve them manually
3. After resolving, run:
   ```powershell
   git add .
   git commit -m "Resolved merge conflicts"
   git push -u origin main
   ```

## Authentication

When prompted for credentials:
- **Username**: `vikrant301io`
- **Password**: Use your GitHub Personal Access Token
  - Get token from: https://github.com/settings/tokens
  - Token needs `repo` scope

## Repository Info

- **URL**: https://github.com/vikrant301io/Appliance-Troubleshoot.git
- **Branch**: main
- **Your Username**: vikrant301io

