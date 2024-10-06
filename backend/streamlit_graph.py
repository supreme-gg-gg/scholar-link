import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import requests

st.set_page_config(
    page_title="Influential Papers Tracker",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main {
        background: #ffffff;
        padding: 3rem;
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

# Input for search keyword
search_keyword = st.text_input("Enter a search keyword:", "")

if search_keyword:
    # Fetch data from Flask API
    api_url = f"http://127.0.0.1:5000/influential_papers?keyword={search_keyword}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            papers_data = response.json()
        else:
            st.error("Failed to fetch data from API.")
            papers_data = []
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")
        papers_data = []

    if papers_data:
        # Create DataFrame
        df = pd.DataFrame(papers_data)
        df = df.sort_values('citations', ascending=True)  # Sort for horizontal bar chart

        # Create the graph
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=df['title'],
            x=df['citations'],
            orientation='h',
            marker=dict(color='#1f4387')
        ))

        # Customize the layout
        fig.update_layout(
            title={
                'text': f"Most Influential Papers for '{search_keyword}'",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=24, color='#1f4387')
            },
            xaxis_title="Number of Citations",
            yaxis_title="Paper Title",
            font=dict(family="Helvetica Neue, Arial", size=14, color="#333333"),
            plot_bgcolor='rgba(240,242,246,0.8)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=600,
            margin=dict(l=200, r=20, t=70, b=70),
        )

        # Update axes
        fig.update_xaxes(
            showgrid=True,
            gridcolor='rgba(200,200,200,0.4)',
        )
        fig.update_yaxes(
            showgrid=False,
            automargin=True,
        )

        # Display the graph
        st.plotly_chart(fig, use_container_width=True)

        # Display table with more details
        st.subheader("Paper Details")
        st.table(df[['title', 'authors', 'year', 'citations']])
    else:
        st.info("No data available for the given keyword. Please try another search term.")
else:
    st.info("Please enter a search keyword to view influential papers.")