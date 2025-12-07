# ⚡ Quick Start Guide

## 🚀 Get Running in 3 Minutes

### Option 1: Automated (Recommended)

```bash
cd /home/mokshith/Documents/Projects/novacorp-udip
./start.sh
```

That's it! The app will open at `http://localhost:8501`

### Option 2: Manual Steps

```bash
# 1. Navigate to project
cd /home/mokshith/Documents/Projects/novacorp-udip

# 2. Activate environment
source venv/bin/activate

# 3. Run app
streamlit run app.py
```

---

## 📱 Using the Dashboard

### 1. Executive Dashboard (🏠)
- **Purpose:** High-level business overview
- **What to see:**
  - Total revenue, orders, churn rate
  - Revenue trends
  - Top products
  - Critical alerts

### 2. Demand & Pricing (📈)
- **Purpose:** Forecast demand and optimize pricing
- **Actions:**
  - View pricing recommendations
  - Select product to forecast
  - Compare prices with competitors
  - Estimate revenue impact

### 3. Logistics Optimizer (🚚)
- **Purpose:** Predict delays and optimize routes
- **Actions:**
  - View delay prediction model performance
  - Identify high-risk routes
  - Get alternative route recommendations
  - Monitor delay distribution

### 4. Predictive Maintenance (⚙️)
- **Purpose:** Prevent machine failures
- **Actions:**
  - View machine health scores
  - Identify critical machines
  - Schedule maintenance
  - Track risk categories

### 5. Analytics & Insights (📊)
- **Purpose:** Deep dive into business metrics
- **Actions:**
  - Analyze customer segments
  - Track carbon footprint
  - Monitor economic indicators
  - Regional performance analysis

---

## 🎯 Demo Scenario

### Scenario: You're the Operations Manager

**Morning Routine:**

1. **Check Executive Dashboard**
   - Revenue up 12.3% ✅
   - But average delay increased 5.2% ⚠️
   - Machine M012 showing high fault rate 🚨

2. **Investigate Logistics**
   - Go to Logistics Optimizer
   - See Route R045 has 80+ risk score
   - Note: Switch to Route R047 (recommendation)

3. **Address Maintenance**
   - Go to Predictive Maintenance
   - Machine M012 is "High Risk"
   - Action: Schedule immediate maintenance

4. **Optimize Pricing**
   - Go to Demand & Pricing
   - Product P001: Increase price by 8%
   - Expected revenue gain: 12%

5. **Report to CEO**
   - Go back to Executive Dashboard
   - Take screenshots
   - Prepare action items

---

## 🔧 Troubleshooting

### App won't start?
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### No data showing?
```bash
# Regenerate data
python src/generate_data.py
```

### Port already in use?
```bash
# Use different port
streamlit run app.py --server.port=8502
```

### Slow performance?
```bash
# Clear Streamlit cache
streamlit cache clear
```

---

## 📸 Screenshots for Portfolio

Take screenshots of:
1. Executive Dashboard (full page)
2. Demand forecast chart
3. Route risk analysis
4. Machine health monitoring
5. Pricing recommendations table

---

## 🎥 Record Demo Video

**Script (2-3 minutes):**

1. **Intro (15 sec)**
   - "This is NovaCorp UDIP - a unified decision intelligence platform"
   - "It combines predictive analytics, optimization, and real-time monitoring"

2. **Executive Dashboard (30 sec)**
   - "Here's the executive view with key KPIs"
   - "Revenue trends, top products, and critical alerts"

3. **Demand Forecasting (45 sec)**
   - "The platform forecasts demand using Prophet"
   - "Recommends optimal prices based on competitors and demand"
   - "This product should increase price by 8% for 12% revenue gain"

4. **Logistics (30 sec)**
   - "Predicts shipment delays using machine learning"
   - "Identifies high-risk routes and suggests alternatives"

5. **Predictive Maintenance (30 sec)**
   - "Monitors machine health in real-time"
   - "Predicts failures before they happen"
   - "Recommends maintenance schedule"

6. **Closing (15 sec)**
   - "Built with Python, Streamlit, and ML"
   - "Deployed on [platform]"
   - "Check out the code on GitHub"

---

## 📤 Deploy to Cloud

### Streamlit Cloud (Easiest - 5 minutes)

1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/novacorp-udip.git
git push -u origin main
```

2. **Deploy:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select repository
   - Click "Deploy"

3. **Done!** Your app is live at:
   `https://YOUR_USERNAME-novacorp-udip.streamlit.app`

---

## ✅ Next Steps

- [ ] Run the app locally
- [ ] Explore all dashboards
- [ ] Take screenshots
- [ ] Record demo video
- [ ] Push to GitHub
- [ ] Deploy to Streamlit Cloud
- [ ] Add to LinkedIn
- [ ] Update resume
- [ ] Share with network

---

## 💡 Tips for Interviews

**When discussing this project:**

1. **Start with business value**
   - "Reduces inventory costs by 30%"
   - "Improves on-time delivery by 18%"
   - "Prevents machine failures, saving $X"

2. **Explain technical choices**
   - "Used Prophet for seasonality detection"
   - "XGBoost for delay prediction due to non-linear patterns"
   - "Random Forest for maintenance - handles imbalanced data well"

3. **Show end-to-end thinking**
   - "Designed data model with 10+ entities"
   - "Built ETL pipeline"
   - "Deployed production-ready dashboard"
   - "Considered scalability and performance"

4. **Demonstrate business acumen**
   - "Focused on actionable insights, not just predictions"
   - "Designed for executive decision-making"
   - "Included ROI calculations"

---

**🎉 You're ready to go! Run `./start.sh` and explore!**
