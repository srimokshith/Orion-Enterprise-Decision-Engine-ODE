#!/bin/bash

echo "🚀 NovaCorp UDIP - Streamlit Cloud Deployment"
echo "=============================================="
echo ""

# Check if in git repo
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
fi

echo "📋 Files to commit:"
git status --short

echo ""
read -p "Continue with deployment? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Deployment cancelled"
    exit 1
fi

echo ""
echo "📦 Adding files..."
git add .

echo "💾 Committing..."
git commit -m "Configure for Streamlit Cloud deployment" || echo "Nothing new to commit"

echo ""
echo "⬆️  Pushing to GitHub..."
git push origin main || git push origin master

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ CODE PUSHED TO GITHUB!"
    echo ""
    echo "🌐 Next Steps:"
    echo "1. Go to: https://share.streamlit.io"
    echo "2. Click 'New app'"
    echo "3. Select repository: srimokshith/Orion-Enterprise-Decision-Engine-ODE-"
    echo "4. Branch: main"
    echo "5. Main file: app.py"
    echo "6. Click 'Deploy!'"
    echo ""
    echo "📱 Your app will be live at:"
    echo "https://srimokshith-orion-enterprise-decision-engine-ode.streamlit.app"
    echo ""
    echo "⏱️  Deployment takes 5-10 minutes"
else
    echo ""
    echo "❌ Push failed. Check your GitHub remote:"
    echo "git remote -v"
fi
