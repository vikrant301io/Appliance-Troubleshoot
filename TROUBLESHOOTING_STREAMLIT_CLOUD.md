# Troubleshooting Streamlit Cloud Deployment Errors

## Error: "Error installing requirements"

This error occurs when Streamlit Cloud cannot install the packages from your `requirements.txt` file.

### Common Causes and Solutions

#### 1. Version Conflicts

**Problem**: Package versions conflict with each other (especially langchain and pydantic).

**Solution**: Use compatible versions. Replace your `requirements.txt` with:

```txt
streamlit>=1.28.0
openai>=1.12.0
python-dotenv>=1.0.0
langchain>=0.1.0,<0.3.0
langchain-openai>=0.0.5,<0.2.0
langchain-core>=0.1.0,<0.3.0
pydantic>=2.0.0,<3.0.0
pydantic-settings>=2.0.0
requests>=2.31.0
Pillow>=10.0.0
typing-extensions>=4.5.0
```

#### 2. Missing Dependencies

**Problem**: Some packages require additional dependencies that aren't listed.

**Solution**: Check the error log in Streamlit Cloud and add missing packages.

#### 3. Platform-Specific Packages

**Problem**: Some packages don't work on Streamlit Cloud's Linux environment.

**Solution**: Remove or replace platform-specific packages.

### Step-by-Step Fix

1. **Check the Error Log**:
   - Go to your app on Streamlit Cloud
   - Click "Manage app" → "Logs"
   - Look for the specific error message

2. **Update requirements.txt**:
   - Use the fixed version below
   - Or use `requirements_fixed.txt` if the error persists

3. **Commit and Push**:
   ```bash
   git add requirements.txt
   git commit -m "Fix requirements.txt for Streamlit Cloud"
   git push origin main
   ```

4. **Redeploy**:
   - Streamlit Cloud will automatically redeploy
   - Or manually trigger a redeploy from the dashboard

### Alternative: Use Fixed Requirements

If you continue to have issues, copy `requirements_fixed.txt` to `requirements.txt`:

```bash
cp requirements_fixed.txt requirements.txt
git add requirements.txt
git commit -m "Use fixed requirements"
git push origin main
```

### Checking Your Requirements

Make sure your `requirements.txt`:
- ✅ Uses correct package names (hyphens, not underscores)
- ✅ Doesn't include Python itself
- ✅ Doesn't include built-in libraries (like `os`, `json`, `datetime`)
- ✅ Has compatible version ranges

### Testing Locally

Before deploying, test locally:

```bash
# Create virtual environment
python -m venv test_env

# Activate (Windows)
test_env\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Test the app
streamlit run streamlit_app.py
```

### Still Having Issues?

1. Check Streamlit Cloud logs for specific error messages
2. Share the error message from the logs
3. Try using `requirements_fixed.txt` which has tested compatible versions

