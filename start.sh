#!/bin/bash

echo "🎯 Starting NovaCorp UDIP..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Check if data exists
if [ ! -f "data/raw/orders.csv" ]; then
    echo "📊 Generating synthetic data..."
    python src/generate_data.py
    echo ""
fi

# Start Streamlit app
echo "🚀 Launching dashboard..."
echo "📱 Open browser at: http://localhost:8501"
echo ""
streamlit run app.py
