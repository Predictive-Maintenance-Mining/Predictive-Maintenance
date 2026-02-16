# 🚀 Render Deployment Checklist

## Quick Reference Guide for Deploying to Render

---

## ✅ Pre-Deployment Checklist

### Files Required
- [ ] **app.py** - Main application file
- [ ] **requirements.txt** - Python dependencies
- [ ] **Procfile** - Deployment command
- [ ] **runtime.txt** - Python version
- [ ] **.streamlit/config.toml** - Streamlit configuration
- [ ] **README.md** - Documentation
- [ ] **.gitignore** - Git ignore rules

### Folders Required
- [ ] **pages/** - Additional pages (truck.py)
- [ ] **output/** - CSV data files
- [ ] **images/** - Image assets
- [ ] **Truck/** - ML model files
- [ ] **pmanalysis/** - Analysis modules

### Code Verification
- [ ] All file paths are **relative** (not absolute)
- [ ] All imports are included in requirements.txt
- [ ] No hardcoded secrets or API keys
- [ ] CSV files are in correct locations
- [ ] Images are in images/ folder

---

## 🔧 Render Configuration Settings

### Service Settings
```
Name: mining-dashboard
Region: Oregon (US West) or closest to users
Branch: main
Root Directory: (leave blank)
Runtime: Python 3
```

### Build & Deploy Commands
```bash
Build Command:
pip install -r requirements.txt

Start Command:
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

### Instance Type
```
Free Tier: $0/month (spins down after 15 min)
Starter: $7/month (always on, recommended)
```

### Environment Variables (Optional)
```
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=10000
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

---

## 📋 Step-by-Step Deployment

### Step 1: GitHub Repository
1. [ ] Create new GitHub repository
2. [ ] Name it (e.g., mining-dashboard)
3. [ ] Keep it **Public** (required for free tier)
4. [ ] Upload all files OR push via Git

### Step 2: Render Setup
1. [ ] Sign in to [dashboard.render.com](https://dashboard.render.com)
2. [ ] Click "New +" → "Web Service"
3. [ ] Connect GitHub account
4. [ ] Select your repository
5. [ ] Click "Connect"

### Step 3: Configuration
1. [ ] Enter service name
2. [ ] Select region
3. [ ] Choose branch (main)
4. [ ] Set build command
5. [ ] Set start command
6. [ ] Select instance type
7. [ ] Add environment variables (optional)

### Step 4: Deploy
1. [ ] Review all settings
2. [ ] Click "Create Web Service"
3. [ ] Wait for build to complete (3-5 minutes)
4. [ ] Check logs for errors
5. [ ] Test the deployed URL

---

## 🎯 Git Commands Quick Reference

### Initial Setup
```bash
cd PM
git init
git add .
git commit -m "Initial commit"
```

### Connect to GitHub
```bash
# Replace YOUR_USERNAME and REPO_NAME
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

### Update Deployment
```bash
git add .
git commit -m "Update dashboard"
git push
```

---

## 🐛 Common Issues & Solutions

### Issue: Build Failed
**Check:**
- [ ] requirements.txt exists
- [ ] All package versions are valid
- [ ] Python version is correct (3.11.7)

**Fix:**
```bash
pip freeze > requirements.txt
```

### Issue: App Won't Start
**Check:**
- [ ] Start command is correct
- [ ] app.py is in root directory
- [ ] No syntax errors in app.py

**Fix:**
- Review Render logs
- Test locally first: `streamlit run app.py`

### Issue: Files Not Found
**Check:**
- [ ] All folders pushed to GitHub
- [ ] File paths are relative
- [ ] CSV files in correct locations

**Fix:**
```python
# Use relative paths
df = pd.read_csv('output/mining_data.csv')  # ✅ Good
df = pd.read_csv('/absolute/path/file.csv')  # ❌ Bad
```

### Issue: Slow Performance
**Solutions:**
- [ ] Upgrade to Starter plan ($7/month)
- [ ] Add caching: `@st.cache_data`
- [ ] Optimize data loading

---

## 📊 Deployment Status Check

### Successful Deployment Shows:
- ✅ "Build successful"
- ✅ "Your service is live"
- ✅ Green status indicator
- ✅ Accessible URL

### Test Your Deployment:
1. [ ] URL opens successfully
2. [ ] Main dashboard loads
3. [ ] All pages accessible
4. [ ] Data displays correctly
5. [ ] Charts render properly
6. [ ] Images show up
7. [ ] No console errors

---

## 🔗 Important URLs

### Your Deployment
```
https://YOUR-SERVICE-NAME.onrender.com
```

### Render Dashboard
```
https://dashboard.render.com
```

### Service Logs
```
Dashboard → Your Service → Logs
```

### Service Metrics
```
Dashboard → Your Service → Metrics
```

---

## 💡 Pro Tips

### Speed Up Deployment
- Keep requirements.txt minimal
- Use Python 3.11 (faster)
- Enable build caching

### Improve Performance
- Use `@st.cache_data` for data loading
- Optimize data processing
- Upgrade to Starter plan

### Monitor Your App
- Check logs regularly
- Monitor metrics
- Set up alerts (paid plans)

### Save Money
- Start with free tier
- Upgrade only if needed
- Use free SSL certificates

---

## 📱 Mobile Testing

After deployment, test on:
- [ ] Desktop browser
- [ ] Tablet
- [ ] Mobile phone
- [ ] Different browsers (Chrome, Firefox, Safari)

---

## 🔐 Security Checklist

- [ ] No secrets in code
- [ ] Use environment variables for sensitive data
- [ ] HTTPS enabled (automatic on Render)
- [ ] No exposed API keys
- [ ] Strong passwords
- [ ] Regular security updates

---

## 📈 Performance Optimization

### Before Deployment
- [ ] Optimize CSV file sizes
- [ ] Compress images
- [ ] Remove unused code
- [ ] Test locally first

### After Deployment
- [ ] Monitor load times
- [ ] Check error logs
- [ ] Optimize slow queries
- [ ] Add caching where needed

---

## 🎉 Post-Deployment Tasks

### Share Your Dashboard
1. [ ] Copy deployment URL
2. [ ] Share with team
3. [ ] Add to documentation
4. [ ] Bookmark it

### Set Up Monitoring
1. [ ] Enable Render metrics
2. [ ] Set up health checks
3. [ ] Configure alerts (paid plans)
4. [ ] Monitor logs regularly

### Documentation
1. [ ] Update README with live URL
2. [ ] Document any custom configuration
3. [ ] Create user guide
4. [ ] Note any known issues

---

## 🆘 Need Help?

### Resources
- 📖 [Render Documentation](https://render.com/docs)
- 📖 [Streamlit Documentation](https://docs.streamlit.io)
- 📧 Render Support: support@render.com
- 💬 Streamlit Forums: discuss.streamlit.io

### Troubleshooting Order
1. Check Render logs
2. Review this checklist
3. Test locally
4. Check GitHub repository
5. Contact support

---

## ✅ Final Verification

Before considering deployment complete:

- [ ] URL is accessible
- [ ] Dashboard loads correctly
- [ ] All pages work
- [ ] Data displays properly
- [ ] Charts render
- [ ] Images show
- [ ] No errors in console
- [ ] Mobile responsive
- [ ] Performance acceptable
- [ ] Team can access it

---

**Deployment Time Estimate:**
- GitHub setup: 5 minutes
- Render configuration: 5 minutes
- Build & deploy: 3-5 minutes
- Testing: 5 minutes
- **Total: 15-20 minutes**

---

**Status:** Ready to Deploy ✅

**Date:** _______________

**Deployed By:** _______________

**URL:** https://_______________

**Notes:** _______________
