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

# Set page configuration for better layout
st.set_page_config(layout="wide")

st.title("Protein Index Dashboard")

# Sidebar for filters
st.sidebar.header("Filter Options")

# Region Multiselect
regions = st.sidebar.multiselect(
    "Select Region",
    options=data['Region'].unique(),
    default=data['Region'].unique()
)

# Protein Index Range Slider
min_index, max_index = st.sidebar.slider(
    "Protein Index Range",
    min_value=0,
    max_value=100,
    value=(50, 100)
)

# Max Cost per gram Slider
max_cost = st.sidebar.slider(
    "Max Cost per gram protein",
    min_value=0.1,
    max_value=1.0,
    value=0.7,
    step=0.05 # Added a step for better control
)

# Apply filters
filtered_data = data[
    (data['Region'].isin(regions)) &
    (data['Protein Index'].between(min_index, max_index)) &
    (data['Cost per gram protein'] <= max_cost)
]

# Display filtered data
st.subheader("Filtered Protein Sources")
if filtered_data.empty:
    st.write("No data matches the selected filters. Please adjust your selections.")
else:
    st.dataframe(filtered_data, use_container_width=True) # use_container_width for better responsiveness

# Create and display scatter plot
st.subheader("Protein Index vs. Cost per gram protein")
fig = px.scatter(
    filtered_data,
    x="Cost per gram protein",
    y="Protein Index",
    color="Food",
    size="Protein Index",
    hover_name="Food", # Shows food name on hover
    title="Protein Index vs. Cost per gram by Food Source"
)
st.plotly_chart(fig, use_container_width=True) # use_container_width for better responsiveness

# Optional: Add some insights or summary
st.subheader("Dashboard Insights")
st.write(f"Currently displaying **{len(filtered_data)}** protein sources out of **{len(data)}** total.")
if not filtered_data.empty:
    st.write(f"Average Protein Index in filtered data: **{filtered_data['Protein Index'].mean():.2f}**")
    st.write(f"Average Cost per gram protein in filtered data: **{filtered_data['Cost per gram protein'].mean():.2f}**")
