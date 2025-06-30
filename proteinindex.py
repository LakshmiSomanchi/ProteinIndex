# app.py

import streamlit as st
import pandas as pd
import plotly.express as px

# --- Sample Data ---
# This data represents protein sources with their index, cost, and region.
# For a full "global food security index" dashboard, you would expand this
# dataset to include all relevant KPIs.
data = pd.DataFrame({
    'Food': ['Lentils', 'Chicken', 'Soy', 'Milk', 'Egg', 'Fish', 'Beef', 'Quinoa'],
    'Protein Index': [78, 85, 92, 50, 88, 82, 75, 90],
    'Cost per gram protein': [0.4, 0.7, 0.5, 0.6, 0.45, 0.65, 0.9, 0.55],
    'Region': ['Asia', 'US', 'Asia', 'Europe', 'US', 'Europe', 'US', 'Asia']
})

# --- Streamlit Page Configuration ---
# Sets the layout to wide for better use of screen real estate.
st.set_page_config(layout="wide", page_title="Protein Index Dashboard")

# --- Dashboard Title ---
st.title("Protein Index & Affordability Dashboard")
st.markdown("A prototype dashboard to identify cost-effective protein-rich foods based on expert research.")

# --- Sidebar for Filters ---
st.sidebar.header("Filter Options")
st.sidebar.markdown("Adjust the sliders and selections below to find the best protein sources.")

# Filter 1: Select Region
# Allows users to select one or more regions.
regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=data['Region'].unique(),
    default=data['Region'].unique(), # Default to all regions selected
    help="Filter foods available in specific regions."
)

# Filter 2: Protein Index Range
# Allows users to define a minimum and maximum protein index.
min_index, max_index = st.sidebar.slider(
    "Protein Index Range",
    min_value=0,
    max_value=100,
    value=(70, 100), # Default to higher protein index
    step=5,
    help="Filter foods by their protein content efficiency (higher is better)."
)

# Filter 3: Max Cost per gram protein
# Allows users to set a maximum cost per gram of protein.
max_cost = st.sidebar.slider(
    "Max Cost per gram protein (USD)",
    min_value=0.1,
    max_value=1.0,
    value=0.7,
    step=0.05,
    help="Filter foods based on their affordability (lower cost is better)."
)

# --- Apply Filters to Data ---
# Filters the DataFrame based on the user's selections.
filtered_data = data[
    (data['Region'].isin(regions)) &
    (data['Protein Index'].between(min_index, max_index)) &
    (data['Cost per gram protein'] <= max_cost)
]

# --- Display Filtered Data ---
st.subheader("Filtered Protein Sources Table")
if filtered_data.empty:
    st.warning("No protein sources match the selected filters. Please adjust your selections.")
else:
    # Display the filtered data in an interactive table.
    st.dataframe(filtered_data, use_container_width=True, height=250) # Set a fixed height for consistency
    # Download button for filtered data
    st.download_button(
        label="Download Filtered Data as CSV",
        data=filtered_data.to_csv(index=False).encode('utf-8'),
        file_name='filtered_protein_sources.csv',
        mime='text/csv',
        help="Download the currently displayed data table."
    )


# --- Create and Display Scatter Plot ---
st.subheader("Protein Index vs. Cost per gram protein")
st.markdown("This chart visualizes the relationship between protein efficiency and cost. Look for items in the top-left quadrant (high protein index, low cost).")

if filtered_data.empty:
    st.info("No data to display in the chart. Adjust filters to see results.")
else:
    fig = px.scatter(
        filtered_data,
        x="Cost per gram protein",
        y="Protein Index",
        color="Food",          # Color points by food type
        size="Protein Index",  # Size points by protein index
        hover_name="Food",     # Show food name on hover
        title="Protein Index vs. Cost per Gram Protein by Food Source",
        labels={
            "Cost per gram protein": "Cost per Gram of Protein (USD)",
            "Protein Index": "Protein Index (Efficiency)"
        },
        template="plotly_white" # Use a clean white background template
    )
    # Customize the plot layout for better readability
    fig.update_layout(
        xaxis_title_standoff=10,
        yaxis_title_standoff=10,
        legend_title="Food Source",
        hovermode="closest"
    )
    # Display the plot.
    st.plotly_chart(fig, use_container_width=True)

# --- Dashboard Insights and Summary ---
st.subheader("Key Insights")
if filtered_data.empty:
    st.info("No insights available as no data matches the current filters.")
else:
    total_foods = len(data)
    displayed_foods = len(filtered_data)

    st.markdown(f"**{displayed_foods}** out of **{total_foods}** protein sources are currently displayed based on your filters.")
    st.markdown(f"**Average Protein Index** of filtered foods: **{filtered_data['Protein Index'].mean():.2f}**")
    st.markdown(f"**Average Cost per gram protein** of filtered foods: **${filtered_data['Cost per gram protein'].mean():.2f}**")

    # Identify the most cost-effective food in the filtered list
    most_cost_effective = filtered_data.loc[filtered_data['Cost per gram protein'].idxmin()]
    st.markdown(f"The most **cost-effective** protein source in the filtered list is **{most_cost_effective['Food']}** (Protein Index: {most_cost_effective['Protein Index']}, Cost: ${most_cost_effective['Cost per gram protein']:.2f}/g protein).")

    # Identify the highest protein index food in the filtered list
    highest_protein_index = filtered_data.loc[filtered_data['Protein Index'].idxmax()]
    st.markdown(f"The protein source with the **highest Protein Index** is **{highest_protein_index['Food']}** (Protein Index: {highest_protein_index['Protein Index']}, Cost: ${highest_protein_index['Cost per gram protein']:.2f}/g protein).")

# --- About Section ---
st.markdown("---")
st.subheader("About This Dashboard")
st.info("This prototype dashboard uses sample data for demonstration. In a full 'global food security index' application, this dataset would be significantly expanded and sourced from relevant nutritional and economic databases. The 'Protein Index' is a conceptual metric for this prototype.")
