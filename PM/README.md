# Mining Industry Dashboard - Deployment Guide

## 🚀 Quick Deploy to Render

This guide will help you deploy your Mining Industry Dashboard to Render in under 10 minutes.

---

## 📋 Prerequisites

Before deploying, make sure you have:
- ✅ A GitHub account
- ✅ A Render account (free tier available at [render.com](https://render.com))
- ✅ Your project files ready

---

## 🎯 Step-by-Step Deployment Process

### Step 1: Prepare Your GitHub Repository

1. **Create a new GitHub repository**
   - Go to [github.com](https://github.com) and sign in
   - Click the "+" icon → "New repository"
   - Name it: `mining-dashboard` (or your preferred name)
   - Keep it **Public** (required for Render free tier)
   - Click "Create repository"

2. **Upload your project files**
   
   **Option A: Using GitHub Web Interface (Easiest)**
   - Click "uploading an existing file"
   - Drag and drop ALL files from your PM folder
   - Make sure to include:
     - ✅ app.py
     - ✅ requirements.txt
     - ✅ Procfile
     - ✅ runtime.txt
     - ✅ setup.sh
     - ✅ .streamlit/config.toml
     - ✅ pages/ folder
     - ✅ output/ folder
     - ✅ images/ folder
     - ✅ data/ folder (if exists)
     - ✅ Truck/ folder
     - ✅ pmanalysis/ folder
   - Add commit message: "Initial commit"
   - Click "Commit changes"

   **Option B: Using Git Commands**
   ```bash
   # Navigate to your PM folder
   cd /path/to/PM
   
   # Initialize git
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit"
   
   # Add remote (replace YOUR_USERNAME and REPO_NAME)
   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

---

### Step 2: Deploy on Render

1. **Go to Render Dashboard**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Sign in (or sign up if you don't have an account)

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"

3. **Connect Your Repository**
   - Click "Connect account" to link GitHub
   - Authorize Render to access your repositories
   - Select your `mining-dashboard` repository
   - Click "Connect"

4. **Configure Your Service**
   
   Fill in the following settings:
   
   **Basic Settings:**
   - **Name**: `mining-dashboard` (or your preferred name)
   - **Region**: Choose closest to your users (e.g., Oregon, Frankfurt, Singapore)
   - **Branch**: `main`
   - **Root Directory**: Leave blank
   - **Runtime**: `Python 3`
   
   **Build & Deploy Settings:**
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   
   - **Start Command**: 
     ```bash
     streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
     ```
   
   **Instance Settings:**
   - **Instance Type**: Select `Free` (for testing) or `Starter` ($7/month for better performance)
   
   **Advanced Settings (Click "Advanced"):**
   - **Auto-Deploy**: `Yes` (automatically deploy on git push)
   - **Health Check Path**: Leave blank

5. **Environment Variables (Optional but Recommended)**
   
   Click "Add Environment Variable" if you need any:
   ```
   Key: STREAMLIT_SERVER_HEADLESS
   Value: true
   
   Key: STREAMLIT_SERVER_PORT
   Value: 10000
   
   Key: STREAMLIT_BROWSER_GATHER_USAGE_STATS
   Value: false
   ```

6. **Create Web Service**
   - Review all settings
   - Click "Create Web Service"
   - Render will start building and deploying your app

---

### Step 3: Monitor Deployment

1. **Watch the Logs**
   - Render will show live deployment logs
   - Look for these success indicators:
     ```
     ==> Building...
     ==> Installing dependencies...
     ==> Build successful!
     ==> Starting service...
     ==> Your service is live!
     ```

2. **Expected Deployment Time**
   - Initial build: 3-5 minutes
   - Subsequent builds: 1-2 minutes

3. **Access Your Dashboard**
   - Once deployed, you'll see: "Your service is live at https://YOUR-APP-NAME.onrender.com"
   - Click the URL to open your dashboard
   - Bookmark it for easy access

---

## 🎉 Your Dashboard is Now Live!

Your dashboard URL will be:
```
https://mining-dashboard-XXXX.onrender.com
```

Share this link with your team!

---

## 🔧 Configuration & Customization

### Custom Domain (Optional)

1. Go to your Render service
2. Click "Settings" → "Custom Domain"
3. Add your domain (e.g., dashboard.yourcompany.com)
4. Follow DNS configuration instructions

### Environment Variables

If you need to add secrets or configuration:
1. Go to "Environment" tab
2. Add variables like:
   - API keys
   - Database URLs
   - Configuration flags

### Scaling Options

**Free Tier:**
- ✅ Good for testing and demos
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ Takes 30-60 seconds to wake up

**Starter ($7/month):**
- ✅ Always running (no spin down)
- ✅ Better performance
- ✅ Faster response times
- ✅ Custom domains included

**Professional ($25/month):**
- ✅ Auto-scaling
- ✅ Better resources
- ✅ Priority support

---

## 📊 Monitoring & Maintenance

### View Logs
```
Render Dashboard → Your Service → Logs
```

Monitor for:
- Deployment status
- Application errors
- Performance issues
- User activity

### Check Metrics
```
Render Dashboard → Your Service → Metrics
```

View:
- CPU usage
- Memory usage
- Response times
- Request counts

### Update Your App

Whenever you make changes:

**Method 1: Push to GitHub**
```bash
git add .
git commit -m "Update dashboard"
git push
```
Render will automatically redeploy!

**Method 2: Manual Deploy**
- Go to Render Dashboard
- Click "Manual Deploy" → "Deploy latest commit"

---

## 🐛 Troubleshooting

### Issue 1: Build Failed
**Error:** `Failed to install requirements`

**Solution:**
```bash
# Check requirements.txt has correct versions
pip freeze > requirements.txt
```

### Issue 2: App Not Starting
**Error:** `Application failed to start`

**Solution:**
- Check logs for specific error
- Verify Procfile command:
  ```
  streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
  ```

### Issue 3: Page Not Found
**Error:** `404 Not Found`

**Solution:**
- Ensure app.py is in root directory
- Check file paths in code are relative
- Verify all CSV files are in correct folders

### Issue 4: Slow Performance
**Problem:** App takes long to load

**Solutions:**
1. Upgrade to Starter plan ($7/month)
2. Optimize data loading with @st.cache_data
3. Reduce initial data processing

### Issue 5: CSV Files Not Found
**Error:** `FileNotFoundError: output/mining_data.csv`

**Solution:**
- Ensure all folders are pushed to GitHub
- Check file paths in code:
  ```python
  # Good: Relative path
  df = pd.read_csv('output/mining_data.csv')
  
  # Bad: Absolute path
  df = pd.read_csv('/Users/yourname/PM/output/mining_data.csv')
  ```

### Issue 6: Images Not Displaying
**Error:** Images don't show up

**Solution:**
- Verify images/ folder is in repository
- Use relative paths:
  ```python
  st.image('images/img1.jpg')  # Good
  st.image('/absolute/path/img1.jpg')  # Bad
  ```

---

## 🔐 Security Best Practices

1. **Don't commit secrets**
   - Use Render environment variables
   - Never commit API keys or passwords

2. **Use HTTPS**
   - Render provides free SSL certificates
   - Your URL will be https://

3. **Authentication (Optional)**
   - Add Streamlit authentication
   - Use Render authentication proxy

---

## 💰 Cost Estimation

### Free Tier
- **Cost:** $0/month
- **Limitations:** 
  - Spins down after 15 min inactivity
  - 750 hours/month free
  - Slower cold starts

### Starter Plan (Recommended)
- **Cost:** $7/month
- **Benefits:**
  - Always running
  - Better performance
  - Custom domains
  - More resources

### Professional Plan
- **Cost:** $25/month
- **Benefits:**
  - Auto-scaling
  - Even better performance
  - Priority support
  - Advanced features

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit on Render Guide](https://render.com/docs/deploy-streamlit-app)

---

## 🎯 Quick Checklist

Before deploying, ensure:
- [ ] All Python files are in repository
- [ ] requirements.txt is up to date
- [ ] Procfile exists and is correct
- [ ] .streamlit/config.toml exists
- [ ] All CSV files are included
- [ ] All image files are included
- [ ] File paths are relative (not absolute)
- [ ] GitHub repository is public (for free tier)
- [ ] No sensitive data in code

---

## 🚀 Alternative Deployment Options

If Render doesn't work for you, try:

### Streamlit Community Cloud (Free)
1. Push to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Deploy

### Heroku
1. Create Heroku account
2. Install Heroku CLI
3. Deploy using Git

### Railway
1. Visit [railway.app](https://railway.app)
2. Connect GitHub
3. Deploy

---

## 📞 Support

If you need help:
1. Check Render logs first
2. Review this troubleshooting guide
3. Check Streamlit forums
4. Contact Render support

---

## ✅ Success Indicators

Your deployment is successful when:
- ✅ Build completes without errors
- ✅ Service status shows "Live"
- ✅ URL opens and shows your dashboard
- ✅ All pages load correctly
- ✅ Data displays properly
- ✅ Charts render correctly
- ✅ No console errors

---

**Ready to deploy? Follow Step 1 above!** 🚀
