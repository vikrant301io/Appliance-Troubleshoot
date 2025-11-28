# Script to push code to GitHub
# Run this script from PowerShell

Write-Host "🚀 Preparing to push code to GitHub..." -ForegroundColor Green

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
} else {
    Write-Host "✅ Git repository already initialized" -ForegroundColor Green
}

# Add remote (remove if exists and add new)
Write-Host "🔗 Setting up remote repository..." -ForegroundColor Yellow
git remote remove origin 2>$null
git remote add origin https://github.com/vikrant301io/Appliance-Troubleshoot.git

# Verify remote
Write-Host "📡 Remote repositories:" -ForegroundColor Cyan
git remote -v

# Stage all files
Write-Host "📝 Staging all files..." -ForegroundColor Yellow
git add .

# Commit
Write-Host "💾 Committing changes..." -ForegroundColor Yellow
git commit -m "Initial commit: Appliance Troubleshoot Agent with Streamlit Cloud deployment ready"

# Set branch to main
Write-Host "🌿 Setting branch to main..." -ForegroundColor Yellow
git branch -M main

# Push to GitHub
Write-Host "⬆️  Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "⚠️  Note: You may be prompted for GitHub credentials (username and Personal Access Token)" -ForegroundColor Red
git push -u origin main

Write-Host ""
Write-Host "✅ Done! Check your repository at: https://github.com/vikrant301io/Appliance-Troubleshoot" -ForegroundColor Green

