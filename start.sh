#!/bin/bash

# West Capital Lending - AI Mortgage Assistant
# Quick Start Script

echo "🏠 West Capital Lending - AI Mortgage Assistant"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo ""
    echo "🔑 Please edit .env and add your OPENAI_API_KEY before continuing."
    echo "   You can edit it with: nano .env"
    echo ""
    read -p "Press Enter when you've added your API key..."
fi

# Start the application
echo ""
echo "🚀 Starting Streamlit application..."
echo "   The app will open in your browser at http://localhost:8501"
echo ""
streamlit run app.py
