#!/bin/bash

echo "🚀 NovaCorp UDIP - Heroku Deployment"
echo "====================================="
echo ""

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found!"
    echo ""
    echo "Install it with:"
    echo "curl https://cli-assets.heroku.com/install.sh | sh"
    echo ""
    echo "Or download from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo "✅ Heroku CLI found"
echo ""

# Check if logged in
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please login to Heroku..."
    heroku login
fi

echo ""
echo "📝 Enter your app name (or press Enter for 'novacorp-udip'):"
read -r app_name

if [ -z "$app_name" ]; then
    app_name="novacorp-udip"
fi

echo ""
echo "🏗️  Creating Heroku app: $app_name"
heroku create "$app_name"

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  App might already exist. Continuing..."
    heroku git:remote -a "$app_name"
fi

echo ""
echo "📦 Committing Heroku deployment files..."
git add Procfile setup.sh runtime.txt
git commit -m "Add Heroku deployment configuration" || echo "Nothing to commit"

echo ""
echo "⬆️  Deploying to Heroku..."
echo "This may take 5-10 minutes..."
git push heroku main || git push heroku master

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ DEPLOYMENT SUCCESSFUL!"
    echo ""
    echo "🌐 Your app is live at:"
    heroku open
    echo ""
    echo "📊 View logs with: heroku logs --tail"
    echo "🔄 Restart with: heroku restart"
else
    echo ""
    echo "❌ Deployment failed. Check logs:"
    echo "heroku logs --tail"
fi
