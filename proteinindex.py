# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Sample Data
data = pd.DataFrame({
    'Food': ['Lentils', 'Chicken', 'Soy', 'Milk', 'Egg'],
    'Protein Index': [78, 85, 92, 50, 88],
    'Cost per gram protein': [0.4, 0.7, 0.5, 0.6, 0.45],
    'Region': ['Asia', 'US', 'Asia', 'Europe', 'US']
})

st.title("Protein Index Dashboard")
st.sidebar.header("Filter")

regions = st.sidebar.multiselect("Select Region", options=data['Region'].unique(), default=data['Region'].unique())
min_index, max_index = st.sidebar.slider("Protein Index Range", 0, 100, (50, 100))
max_cost = st.sidebar.slider("Max Cost per gram", 0.1, 1.0, 0.7)

filtered_data = data[
    (data['Region'].isin(regions)) &
    (data['Protein Index'].between(min_index, max_index)) &
    (data['Cost per gram protein'] <= max_cost)
]

st.subheader("Filtered Protein Sources")
st.dataframe(filtered_data)

fig = px.scatter(filtered_data, x="Cost per gram protein", y="Protein Index", color="Food", size="Protein Index")
st.plotly_chart(fig)
