import streamlit as st
import plotly.express as px
import pandas as pd
import requests


st.set_page_config(page_title="Keyword Frequencies", layout="wide")


# Fetch data from Flask API
api_url = "http://127.0.0.1:5000/paper_keywords?keyword={search_keyword}"
try:
    response = requests.post(api_url, json={"index": st.session_state.get('paper_index', 0)})
    if response.status_code == 200:
        data = response.json()
        keyword_frequencies = data['keyword_frequencies']
    else:
        st.error("Failed to fetch data from API.")
        keyword_frequencies = {}
except Exception as e:
    st.error(f"Error occurred: {str(e)}")
    keyword_frequencies = {}


# Create DataFrame
df = pd.DataFrame(list(keyword_frequencies.items()), columns=['Keyword', 'Frequency'])
df = df.sort_values('Frequency', descending=True)


# Create the graph
fig = px.bar(df, x='Keyword', y='Frequency', title="Keyword Frequencies")
fig.update_layout(xaxis_title="Keywords", yaxis_title="Frequency")


# Display the graph
st.plotly_chart(fig, use_container_width=True)