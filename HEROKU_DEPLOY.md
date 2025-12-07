# 🚀 Heroku Deployment Guide

## Prerequisites

1. **Heroku Account** - Sign up at https://heroku.com (FREE tier available)
2. **Heroku CLI** - Install from https://devcenter.heroku.com/articles/heroku-cli

## Step-by-Step Deployment

### 1. Install Heroku CLI

**Linux/Mac:**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

**Or download from:** https://devcenter.heroku.com/articles/heroku-cli

### 2. Login to Heroku

```bash
heroku login
```

This will open a browser window. Login with your Heroku credentials.

### 3. Navigate to Project

```bash
cd /home/mokshith/Documents/Projects/novacorp-udip
```

### 4. Create Heroku App

```bash
heroku create novacorp-udip
```

Or with custom name:
```bash
heroku create your-custom-name
```

### 5. Push Code to GitHub (if not done)

```bash
git add .
git commit -m "Add Heroku deployment files"
git push origin main
```

### 6. Deploy to Heroku

```bash
git push heroku main
```

If you're on a different branch:
```bash
git push heroku your-branch:main
```

### 7. Open Your App

```bash
heroku open
```

Or visit: `https://novacorp-udip.herokuapp.com`

---

## 🔧 Troubleshooting

### Error: "No such app"
```bash
heroku apps
heroku git:remote -a your-app-name
```

### Error: "Application error"
Check logs:
```bash
heroku logs --tail
```

### Error: "Slug size too large"
Your app might be too big. Check:
```bash
heroku builds:info
```

If data files are too large, consider:
- Uploading data to S3/cloud storage
- Generating data on first run
- Using smaller sample datasets

### Memory Issues

Upgrade to Hobby dyno ($7/month):
```bash
heroku ps:scale web=1:hobby
```

---

## 📊 Monitor Your App

```bash
# View logs
heroku logs --tail

# Check app status
heroku ps

# Restart app
heroku restart

# Open dashboard
heroku open
```

---

## 💰 Cost

**Free Tier:**
- 550-1000 dyno hours/month
- App sleeps after 30 min of inactivity
- Wakes up on first request (may take 10-30 seconds)

**Hobby Tier ($7/month):**
- Never sleeps
- Custom domains
- Better performance

---

## 🎯 Quick Commands Reference

```bash
# Create app
heroku create app-name

# Deploy
git push heroku main

# View logs
heroku logs --tail

# Open app
heroku open

# Restart
heroku restart

# Delete app
heroku apps:destroy app-name
```

---

## ✅ Files Created for Heroku

- ✅ `Procfile` - Tells Heroku how to run your app
- ✅ `setup.sh` - Configures Streamlit for Heroku
- ✅ `runtime.txt` - Specifies Python version
- ✅ `requirements.txt` - Already exists

---

## 🌐 Your App URL

After deployment:
`https://your-app-name.herokuapp.com`

---

## 🔄 Update Your App

After making changes:

```bash
git add .
git commit -m "Update description"
git push heroku main
```

Heroku will automatically rebuild and redeploy.

---

## 📱 Alternative: Use Heroku Dashboard

1. Go to https://dashboard.heroku.com
2. Click "New" → "Create new app"
3. Connect to GitHub repository
4. Enable automatic deploys
5. Click "Deploy Branch"

---

**Ready to deploy? Run these commands:**

```bash
cd /home/mokshith/Documents/Projects/novacorp-udip
heroku login
heroku create novacorp-udip
git push heroku main
heroku open
```

🎉 Your app will be live in 5-10 minutes!
