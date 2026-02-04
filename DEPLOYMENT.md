# Deployment Guide

## Deploying to Posit Cloud/Connect

### Prerequisites
- GitHub account linked to Posit
- Repository: `dylanmatthews/census-permit-data`

### Option 1: Deploy via Posit Web Interface (Recommended)

1. **Go to Posit Cloud/Connect**
   - Navigate to your Posit dashboard
   - URL: https://posit.cloud or your Connect server URL

2. **Create New Deployment**
   - Click "New Project" or "Publish Content"
   - Select "Import from Git Repository"

3. **Configure**
   - **Repository**: `dylanmatthews/census-permit-data`
   - **Branch**: `main`
   - **Type**: Python - Streamlit
   - **Entry Point**: `app.py`

4. **Deploy**
   - Posit will automatically detect `requirements.txt`
   - Click "Deploy" and wait for build to complete
   - Your app will be available at a public URL

### Option 2: Deploy via CLI

```bash
# Install rsconnect-python
pip install rsconnect-python

# Add your Posit server (first time only)
rsconnect add \
  --name posit \
  --server https://your-posit-server.com \
  --api-key YOUR_API_KEY

# Deploy the app
rsconnect deploy streamlit \
  --name posit \
  --entrypoint app.py \
  --title "Census Building Permits Explorer" \
  .
```

### Files Included in Deployment
- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `historical_data/processed/six_metros_2000_2024_combined.csv` - Data file
- `manifest.json` - Deployment configuration

### Environment Requirements
- **Python**: 3.9+
- **Memory**: 512 MB minimum (1 GB recommended)
- **Storage**: ~50 MB for data file

### Deployment Settings

**Recommended Configuration:**
- **Idle timeout**: 15 minutes
- **Max processes**: 1
- **Max connections per process**: 50
- **Access**: Public (or as needed)

### Troubleshooting

**If deployment fails:**

1. **Check requirements.txt** - Ensure all versions are compatible
2. **Check file paths** - Verify `historical_data/processed/` exists
3. **Check Python version** - Must be 3.9+
4. **Check logs** - Review deployment logs in Posit dashboard

**Common Issues:**

- **"Module not found"**: Add missing package to `requirements.txt`
- **"File not found"**: Ensure data file is committed to git
- **"Memory exceeded"**: Increase memory allocation in settings

### Post-Deployment

After successful deployment:

1. **Test the app** - Open the provided URL and test both modes
2. **Configure access** - Set permissions (public/private)
3. **Set up monitoring** - Enable usage tracking if available
4. **Share the link** - Add URL to README.md

### Alternative: Streamlit Community Cloud

If you prefer Streamlit's native hosting:

1. Go to https://share.streamlit.io
2. Connect your GitHub account
3. Select repository: `dylanmatthews/census-permit-data`
4. Set main file: `app.py`
5. Deploy

**Note**: Streamlit Community Cloud is free and specifically optimized for Streamlit apps.

## Updating the Deployment

When you push changes to GitHub:

**Auto-deploy (if enabled):**
- Changes to `main` branch automatically redeploy

**Manual redeploy:**
- Go to Posit dashboard
- Find your app
- Click "Redeploy" or "Pull from Git"

## Support

- **Posit Support**: https://support.posit.co
- **Streamlit Docs**: https://docs.streamlit.io
- **This Project**: https://github.com/dylanmatthews/census-permit-data/issues
