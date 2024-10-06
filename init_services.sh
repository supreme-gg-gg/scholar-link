#!/bin/bash

echo "Starting npm..."
cd frontend
npm start &

echo "Starting Streamlit Trend Graph"
cd ../backend
streamlit run streamlit_graph.py --server.port 8501&

echo "Starting Streamlit Bar Graph"
streamlit run streamlit_bargraph.py --server.port 8503&

echo "Starting Streamlit Chatbot"
streamlit run streamlit_chatbot.py --server.port 8502&

echo "Starting Flask..."
cd ..
python3 backend/server.py &

wait
