import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(page_title="Research Activity Tracker", layout="wide")

# Custom CSS to make it look beautiful
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
</style>
""", unsafe_allow_html=True)

# Title
st.title("Research Activity Tracker")

# Generate sample data
dates = pd.date_range(start="2010-01-01", end="2023-12-31", freq="M")
activity = np.cumsum(np.random.randint(1, 10, size=len(dates)))

# Create DataFrame
df = pd.DataFrame({"Date": dates, "Activity": activity})

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
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=24, color='#1f4387')
    },
    xaxis_title="Time",
    yaxis_title="Activity",
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

# Add some explanatory text
st.markdown("""
This graph displays the cumulative research activity in a certain field over time. 
The x-axis represents the timeline, while the y-axis shows the activity level. 
You can use the range slider at the bottom to zoom in on specific time periods, 
or use the buttons above the graph to quickly select common time ranges.

The smooth curve indicates a steady increase in research activity over the years, 
with some periods showing more rapid growth than others. This visualization helps 
in identifying trends and patterns in the research field's development over time.
""")