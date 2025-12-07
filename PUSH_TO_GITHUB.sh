#!/bin/bash

echo "🚀 NovaCorp UDIP - GitHub Push Script"
echo "======================================"
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
fi

echo "📋 Files to be committed:"
git add -n . | wc -l
echo ""

echo "⚠️  BEFORE RUNNING THIS:"
echo "1. Create repository on GitHub: https://github.com/new"
echo "2. Repository name: novacorp-udip"
echo "3. Keep it PUBLIC"
echo "4. DON'T initialize with README"
echo ""

read -p "Have you created the GitHub repository? (y/n) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Please create the repository first, then run this script again."
    exit 1
fi

echo ""
read -p "Enter your GitHub username: " username

if [ -z "$username" ]; then
    echo "❌ Username cannot be empty"
    exit 1
fi

echo ""
echo "📦 Adding files..."
git add .

echo "💾 Committing..."
git commit -m "Initial commit: NovaCorp UDIP - Decision Intelligence Platform

- 3 ML models (Prophet, XGBoost, Random Forest)
- 5 interactive dashboards
- 150K+ data points
- Complete documentation
- Deployment ready"

echo "🔗 Adding remote..."
git remote add origin https://github.com/$username/novacorp-udip.git

echo "⬆️  Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ SUCCESS! Your code is now on GitHub!"
echo ""
echo "📍 Repository URL: https://github.com/$username/novacorp-udip"
echo ""
echo "🌐 Next step: Deploy to Streamlit Cloud"
echo "   1. Go to: https://share.streamlit.io"
echo "   2. Click 'New app'"
echo "   3. Select your repository"
echo "   4. Click 'Deploy'"
echo ""
echo "🎉 Your live URL will be: https://$username-novacorp-udip.streamlit.app"
