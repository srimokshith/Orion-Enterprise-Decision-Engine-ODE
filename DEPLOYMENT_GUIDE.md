# 🚀 Deployment Guide - NovaCorp UDIP

## Quick Start (Local)

```bash
# 1. Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Generate data
python src/generate_data.py

# 3. Run app
streamlit run app.py
```

## 🌐 Deploy to Streamlit Cloud (RECOMMENDED - FREE)

### Step 1: Prepare Repository

1. **Create GitHub repository**
```bash
cd novacorp-udip
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/novacorp-udip.git
git push -u origin main
```

2. **Ensure these files exist:**
- `requirements.txt`
- `app.py`
- `data/raw/` (with generated CSV files)

### Step 2: Deploy

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository: `YOUR_USERNAME/novacorp-udip`
4. Main file path: `app.py`
5. Click "Deploy"

**Your app will be live at:** `https://YOUR_USERNAME-novacorp-udip.streamlit.app`

### Step 3: Configure (Optional)

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 200
```

---

## 🐳 Deploy with Docker

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build
docker build -t novacorp-udip .

# Run
docker run -p 8501:8501 novacorp-udip
```

---

## ☁️ Deploy to AWS EC2

### Step 1: Launch EC2 Instance

1. Go to AWS Console → EC2
2. Launch instance:
   - AMI: Ubuntu 22.04
   - Instance type: t2.medium (or t2.small)
   - Security group: Allow port 8501

### Step 2: Connect and Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Clone repository
git clone https://github.com/YOUR_USERNAME/novacorp-udip.git
cd novacorp-udip

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate data
python src/generate_data.py
```

### Step 3: Run with PM2 (Process Manager)

```bash
# Install Node.js and PM2
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g pm2

# Create startup script
cat > start.sh << 'EOF'
#!/bin/bash
source venv/bin/activate
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
EOF

chmod +x start.sh

# Start with PM2
pm2 start start.sh --name novacorp-udip
pm2 save
pm2 startup
```

### Step 4: Setup Nginx (Optional - for custom domain)

```bash
sudo apt install nginx -y

# Create Nginx config
sudo nano /etc/nginx/sites-available/novacorp

# Add this configuration:
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/novacorp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Access:** `http://<EC2_PUBLIC_IP>:8501` or `http://your-domain.com`

---

## 🔥 Deploy to Heroku

### Step 1: Prepare Files

Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

### Step 2: Deploy

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create novacorp-udip

# Deploy
git push heroku main

# Open app
heroku open
```

---

## 🌊 Deploy to DigitalOcean App Platform

### Step 1: Prepare

1. Push code to GitHub
2. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)

### Step 2: Create App

1. Click "Create App"
2. Connect GitHub repository
3. Configure:
   - **Build Command:** `pip install -r requirements.txt && python src/generate_data.py`
   - **Run Command:** `streamlit run app.py --server.port=8080`
   - **Port:** 8080

### Step 3: Deploy

Click "Deploy" - Your app will be live in 5-10 minutes!

---

## 📊 Performance Optimization

### For Production Deployment:

1. **Enable Caching**
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    # ... data loading code
```

2. **Use PostgreSQL Instead of CSV**
```python
import psycopg2
conn = psycopg2.connect(DATABASE_URL)
df = pd.read_sql("SELECT * FROM orders", conn)
```

3. **Optimize Data Loading**
```python
# Load only required columns
df = pd.read_csv('data.csv', usecols=['col1', 'col2'])

# Use chunking for large files
chunks = pd.read_csv('data.csv', chunksize=10000)
```

4. **Add Loading Indicators**
```python
with st.spinner('Loading...'):
    # Long-running operation
```

---

## 🔒 Security Best Practices

### 1. Environment Variables

Create `.env`:
```
DATABASE_URL=postgresql://user:pass@host:5432/db
API_KEY=your_secret_key
```

Load in app:
```python
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv('DATABASE_URL')
```

### 2. Add Authentication (Streamlit)

```python
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    credentials,
    'cookie_name',
    'signature_key',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show app
    st.write(f'Welcome {name}')
else:
    st.error('Username/password is incorrect')
```

---

## 📈 Monitoring & Analytics

### Add Google Analytics

Create `.streamlit/config.toml`:
```toml
[browser]
gatherUsageStats = true
```

### Add Custom Logging

```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info('User accessed dashboard')
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
```bash
pip install --upgrade -r requirements.txt
```

### Issue: "Port already in use"
```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run app.py --server.port=8502
```

### Issue: "Memory error"
```bash
# Reduce data size or use sampling
df = pd.read_csv('data.csv').sample(frac=0.1)
```

---

## ✅ Pre-Deployment Checklist

- [ ] All dependencies in `requirements.txt`
- [ ] Data files generated (`python src/generate_data.py`)
- [ ] App runs locally without errors
- [ ] README.md updated with project details
- [ ] Sensitive data removed (no API keys in code)
- [ ] `.gitignore` configured properly
- [ ] Code committed to GitHub
- [ ] Screenshots/demo video prepared

---

## 🎥 Create Demo Video

Use **OBS Studio** or **Loom**:

1. Record 2-3 minute walkthrough
2. Show each dashboard page
3. Demonstrate key features
4. Explain business value
5. Upload to YouTube (unlisted)
6. Add link to README

---

## 📞 Support

If you encounter issues:
1. Check Streamlit logs
2. Review GitHub Issues
3. Streamlit Community Forum
4. Stack Overflow

---

**🎉 Congratulations! Your app is now live!**

Share your deployment URL:
- On LinkedIn
- In your resume
- With potential employers
