# ⚡ Quick Start - Deploy in 10 Minutes

## 🎯 Three Simple Steps to Deploy Your Dashboard

---

## Step 1️⃣: Upload to GitHub (3 minutes)

### Option A: Web Upload (Easiest)
1. Go to **https://github.com/new**
2. Name your repo: `mining-dashboard`
3. Keep it **Public** ✓
4. Click **"Create repository"**
5. Click **"uploading an existing file"**
6. Drag ALL files from your PM folder
7. Click **"Commit changes"**

### Option B: Git Commands
```bash
cd PM
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/mining-dashboard.git
git branch -M main
git push -u origin main
```

**✅ Done! Your code is on GitHub**

---

## Step 2️⃣: Connect to Render (2 minutes)

1. Go to **https://dashboard.render.com**
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect GitHub"** (authorize if needed)
4. Find and select **"mining-dashboard"**
5. Click **"Connect"**

**✅ Done! Repository connected**

---

## Step 3️⃣: Configure & Deploy (5 minutes)

### Fill in these fields:

**Name:** 
```
mining-dashboard
```

**Region:**
```
Oregon (US West)  [or closest to you]
```

**Branch:**
```
main
```

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**Instance Type:**
```
Free  (or Starter - $7/month for better performance)
```

### Click **"Create Web Service"**

**✅ Done! Deploying...**

---

## 🎉 That's It!

Wait 3-5 minutes for deployment.

Your dashboard will be live at:
```
https://mining-dashboard-XXXX.onrender.com
```

---

## 🐛 Quick Troubleshooting

### Build Failed?
- Check all files are in GitHub
- Verify requirements.txt exists

### Can't See Your Repo?
- Make sure repository is Public
- Try disconnecting and reconnecting GitHub

### App Won't Start?
- Check Render logs for errors
- Verify app.py is in root folder

---

## 💡 Next Steps

### To Update Your App:
```bash
git add .
git commit -m "Update"
git push
```
Render will auto-deploy! 🚀

### To Upgrade Performance:
- Go to Settings → Instance Type
- Change to "Starter" ($7/month)
- No more spin-down delays!

---

## 📞 Need More Help?

See full guide: **README.md**

---

**Time to Deploy:** 10 minutes  
**Cost:** Free (or $7/month for Starter)  
**Difficulty:** Easy ⭐⭐☆☆☆
