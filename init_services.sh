#!/bin/bash

# Function to kill all background processes when the script exits
cleanup() {
    echo "Stopping all services..."
    pkill -P $$  # Kill all background processes spawned by this script
}

# Trap EXIT signal to trigger cleanup
trap cleanup EXIT

echo "Starting npm..."
cd frontend || exit 1
npm start > npm.log 2>&1 &

echo "Starting Flask..."
cd ../backend || exit 1
python3 server.py > flask.log 2>&1 &

echo "Starting Streamlit Trend Graph"
streamlit run streamlit_graph.py --server.port 8501 > trend_graph.log 2>&1 &

echo "Starting Streamlit Bar Graph"
streamlit run streamlit_bargraph.py --server.port 8503 > bargraph.log 2>&1 &

echo "Starting Streamlit Chatbot"
streamlit run streamlit_chatbot.py --server.port 8502 > chatbot.log 2>&1 &

echo "All services started. Check logs for details."

# Wait for all background jobs
wait