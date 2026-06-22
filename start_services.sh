#!/bin/bash

# Start services for the Multi-Agent Loan Approval System

echo "🚀 Starting Multi-Agent Loan Approval System"
echo "=============================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Set environment variables
export ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-"your_api_key_here"}

# Start FastAPI service in background
echo ""
echo "🌐 Starting FastAPI microservice on http://127.0.0.1:8000..."
python fastapi_service.py &
FASTAPI_PID=$!

# Wait for API to start
sleep 3

# Start Streamlit
echo "🎨 Starting Streamlit UI on http://127.0.0.1:8501..."
streamlit run streamlit_app.py

# Cleanup on exit
trap "kill $FASTAPI_PID" EXIT
