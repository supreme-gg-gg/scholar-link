import requests
import streamlit as st
import os
from dotenv import load_dotenv
# Load environment variables from a .env file
load_dotenv()
api_key = os.getenv("API_KEY")

# Streamlit interface
st.title("Ask the Paper...")

# Create a placeholder for the PDF URL
# pdf_url = st.query_params["data_url"] or st.empty()
try:
    response = requests.get("http://127.0.0.1:5000/get-url")
    pdf_url = response.json().get("url")
except:
    st.write("Click on an entry to chat with it!")

source_id = ""
headers = {
    'x-api-key': api_key,
    "Content-Type": "application/json",
}

st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main {
        background: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1 {
        color: #1f4387;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stPlotlyChart {
        background: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def post_pdf(url):

    data = {'url': url}

    response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-url', headers=headers, json=data)

    if response.status_code == 200:
        global source_id
        source_id = response.json()['sourceId']
        return True
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        return False

def query_message(content):

    global source_id
    if source_id == "":
        return False

    data = {
        'sourceId': source_id,
        'messages': [
            {
                'role': "user",
                'content': content,
            }
        ]
    }

    response = requests.post(
        'https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['content']
    else:
        print('Status:', response.status_code)
        print('Error:', response.text)
        return False

if pdf_url:

    if post_pdf(pdf_url):
        st.success("Paper Loaded Successfully!")

    user_input = st.text_input("Ask a question about the research paper:")

    if user_input:
            # Provide the scientific paper context and generate a response
            ai_response = query_message(user_input)
            st.text_area("Chatbot Response:", value=ai_response, height=300, disabled=True)
