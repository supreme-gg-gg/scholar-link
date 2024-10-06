#!/bin/bash

echo "Starting npm..."
cd frontend
npm start &

echo "Starting Streamlit Graph"
cd ../backend
streamlit run streamlit_graph.py &

echo "Starting Streamlit Chatbot"
streamlit run streamlit_chatbot.py &

echo "Starting Flask..."
cd ..
python3 backend/server.py &

wait
