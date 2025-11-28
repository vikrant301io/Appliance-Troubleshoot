# Script to pull from main branch first, then push code to GitHub
# Run this script from PowerShell

Write-Host "🚀 Pulling from main branch and pushing code to GitHub..." -ForegroundColor Green

# Check if git is initialized
if (-not (Test-Path .git)) {
    Write-Host "📦 Initializing Git repository..." -ForegroundColor Yellow
    git init
    git branch -M main
}

# Add remote (remove if exists and add new)
Write-Host "🔗 Setting up remote repository..." -ForegroundColor Yellow
$remoteExists = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Remote already exists, updating..." -ForegroundColor Yellow
    git remote set-url origin https://github.com/vikrant301io/Appliance-Troubleshoot.git
} else {
    Write-Host "Adding remote..." -ForegroundColor Yellow
    git remote add origin https://github.com/vikrant301io/Appliance-Troubleshoot.git
}

# Verify remote
Write-Host "📡 Remote repositories:" -ForegroundColor Cyan
git remote -v

# Fetch from remote first
Write-Host "📥 Fetching from remote repository..." -ForegroundColor Yellow
git fetch origin main

# Check if main branch exists on remote
Write-Host "🔍 Checking remote main branch..." -ForegroundColor Yellow

# Pull from main branch (allow unrelated histories if needed)
Write-Host "⬇️  Pulling from main branch..." -ForegroundColor Yellow
Write-Host "⚠️  If there are conflicts, you may need to resolve them manually" -ForegroundColor Red

# Try to pull with rebase first, if that fails, try merge
git pull origin main --allow-unrelated-histories 2>&1 | Out-String
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Pull failed or branch doesn't exist yet. Continuing with push..." -ForegroundColor Yellow
}

# Stage all files
Write-Host "📝 Staging all files..." -ForegroundColor Yellow
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    Write-Host "💾 Committing changes..." -ForegroundColor Yellow
    git commit -m "Update: Appliance Troubleshoot Agent with Streamlit Cloud deployment ready"
} else {
    Write-Host "✅ No changes to commit" -ForegroundColor Green
}

# Set branch to main
Write-Host "🌿 Ensuring branch is set to main..." -ForegroundColor Yellow
git branch -M main

# Push to GitHub
Write-Host "⬆️  Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "⚠️  Note: You may be prompted for GitHub credentials (username and Personal Access Token)" -ForegroundColor Red
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "🔗 Repository: https://github.com/vikrant301io/Appliance-Troubleshoot" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "❌ Push failed. Please check the error messages above." -ForegroundColor Red
    Write-Host "💡 Common issues:" -ForegroundColor Yellow
    Write-Host "   - Authentication failed: Use a Personal Access Token instead of password" -ForegroundColor Yellow
    Write-Host "   - Conflicts: Resolve conflicts and try again" -ForegroundColor Yellow
}

