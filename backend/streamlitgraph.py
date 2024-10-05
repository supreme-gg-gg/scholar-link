import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import requests

st.set_page_config(
    page_title="Research Activity Tracker",
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

# Fetch data from Flask API
api_url = "http://127.0.0.1:5000/graphdata"
try:
    response = requests.get(api_url)
    if response.status_code == 200:
        input_data = response.json()
    else:
        st.error("Failed to fetch data from API.")
        print(st.error)
        input_data = []
except Exception as e:
    st.error(f"Error occurred: {str(e)}")
    input_data = []

# Generate date range for the DataFrame
dates = pd.date_range(start="2010-01-01", end="2023-12-31", freq="MS")
activity = np.zeros(len(dates))

# Create DataFrame
df = pd.DataFrame({"Date": dates, "Activity": activity})

def update_activity(input_data):
    """Updates the activity DataFrame based on the input data."""
    for date_str, value in input_data:
        date = pd.to_datetime(date_str).normalize().replace(day=1).tz_localize(None)
        
        mask = df['Date'] == date
        
        if mask.any():
            df.loc[mask, 'Activity'] += value 
        else:
            st.warning(f"Date {date_str} is not in the range of the dataset or formatted correctly.")



# Update the DataFrame with the input data fetched from API
update_activity(input_data)

# Create the graph
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['Date'],
    y=df['Activity'],
    mode='lines+markers',
    name='Research Activity',
    line=dict(color='#1f4387', width=3),
    marker=dict(size=8, color='#1f4387', symbol='circle')
))

# Customize the layout
fig.update_layout(
    title={
        'text': "Research Activity Over Time",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=24, color='#1f4387')
    },
    xaxis_title="Time",
    yaxis_title="Activity (citations)",
    font=dict(family="Helvetica Neue, Arial", size=14, color="#333333"),
    plot_bgcolor='rgba(240,242,246,0.8)',
    paper_bgcolor='rgba(0,0,0,0)',
    hovermode='x unified',
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(200,200,200,0.4)',
        tickformat='%b %Y'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='rgba(200,200,200,0.4)',
    ),
)

# Add range slider and selector
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(count=5, label="5y", step="year", stepmode="backward"),
            dict(count=10, label="10y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)

# Display the graph
st.plotly_chart(fig, use_container_width=True)
