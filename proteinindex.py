# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.components.v1 import html # Import html component for embedding

# --- Sample Data ---
data = pd.DataFrame({
    'Food': ['Lentils', 'Chicken', 'Soy', 'Milk', 'Egg', 'Fish', 'Beef', 'Quinoa'],
    'Protein Index': [78, 85, 92, 50, 88, 82, 75, 90],
    'Cost per gram protein': [0.4, 0.7, 0.5, 0.6, 0.45, 0.65, 0.9, 0.55],
    'Region': ['Asia', 'US', 'Asia', 'Europe', 'US', 'Europe', 'US', 'Asia']
})

# --- Streamlit Page Configuration ---
st.set_page_config(layout="wide", page_title="Protein Index Dashboard")

# --- Dashboard Title ---
st.title("Protein Index & Affordability Dashboard")
st.markdown("A prototype dashboard to identify cost-effective protein-rich foods based on expert research.")

# --- Sidebar for Filters ---
st.sidebar.header("Filter Options")
st.sidebar.markdown("Adjust the sliders and selections below to find the best protein sources.")

# Filter 1: Select Region
regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=data['Region'].unique(),
    default=data['Region'].unique(),
    help="Filter foods available in specific regions."
)

# Filter 2: Protein Index Range
min_index, max_index = st.sidebar.slider(
    "Protein Index Range",
    min_value=0,
    max_value=100,
    value=(70, 100),
    step=5,
    help="Filter foods by their protein content efficiency (higher is better)."
)

# Filter 3: Max Cost per gram protein
max_cost = st.sidebar.slider(
    "Max Cost per gram protein (USD)",
    min_value=0.1,
    max_value=1.0,
    value=0.7,
    step=0.05,
    help="Filter foods based on their affordability (lower cost is better)."
)

# --- Apply Filters to Data ---
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
    st.dataframe(filtered_data, use_container_width=True, height=250)
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
        color="Food",
        size="Protein Index",
        hover_name="Food",
        title="Protein Index vs. Cost per Gram Protein by Food Source",
        labels={
            "Cost per gram protein": "Cost per Gram of Protein (USD)",
            "Protein Index": "Protein Index (Efficiency)"
        },
        template="plotly_white"
    )
    fig.update_layout(
        xaxis_title_standoff=10,
        yaxis_title_standoff=10,
        legend_title="Food Source",
        hovermode="closest"
    )
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

    most_cost_effective = filtered_data.loc[filtered_data['Cost per gram protein'].idxmin()]
    st.markdown(f"The most **cost-effective** protein source in the filtered list is **{most_cost_effective['Food']}** (Protein Index: {most_cost_effective['Protein Index']}, Cost: ${most_cost_effective['Cost per gram protein']:.2f}/g protein).")

    highest_protein_index = filtered_data.loc[filtered_data['Protein Index'].idxmax()]
    st.markdown(f"The protein source with the **highest Protein Index** is **{highest_protein_index['Food']}** (Protein Index: {highest_protein_index['Protein Index']}, Cost: ${highest_protein_index['Cost per gram protein']:.2f}/g protein).")


# --- Maps Section ---
st.subheader("Global Food Security Visualizations")
st.markdown("Select the maps below to view different aspects of global food security and relevant initiatives.")

# Define the HTML embed codes for each map
# IMPORTANT: I've used the provided codes. Please double-check the 'Action needed' map code
# as it was identical to 'Technoserve\'s Presence' in your original request.
map_embed_codes = {
    "GFSI World Hunger Data": """
    <div style="min-height:369px; width:100%" id="datawrapper-vis-d0yRp"><script type="text/javascript" defer src="https://datawrapper.dwcdn.net/d0yRp/embed.js" charset="utf-8" data-target="#datawrapper-vis-d0yRp"></script><noscript><img src="https://datawrapper.dwcdn.net/d0yRp/full.png" alt="" /></noscript></div>
    """,
    "Technoserve's Presence": """
    <div style="min-height:330px; width:100%" id="datawrapper-vis-pf5wv"><script type="text/javascript" defer src="https://datawrapper.dwcdn.net/pf5wv/embed.js" charset="utf-8" data-target="#datawrapper-vis-pf5wv"></script><noscript><img src="https://datawrapper.dwcdn.net/pf5wv/full.png" alt="" /></noscript></div>
    """,
    "Action Needed (Check Code)": """
    <div style="min-height:555px; width:100%" id="datawrapper-vis-pf5wv"><script type="text/javascript" defer src="https://datawrapper.dwcdn.net/pf5wv/embed.js" charset="utf-8" data-target="#datawrapper-vis-pf5wv"></script><noscript><img src="https://datawrapper.dwcdn.net/pf5wv/full.png" alt="" /></noscript></div>
    """
}

# Add checkboxes for map selection
st.sidebar.header("Map Options")
show_gfsi = st.sidebar.checkbox("Show GFSI World Hunger Data Map", value=True)
show_technoserve = st.sidebar.checkbox("Show Technoserve's Presence Map")
show_action_needed = st.sidebar.checkbox("Show Action Needed Map (Verify Code)", help="Please verify this map's embed code if it's different from Technoserve's.")


# Display maps based on checkbox selection
if show_gfsi:
    st.markdown("#### GFSI World Hunger Data")
    html(map_embed_codes["GFSI World Hunger Data"], height=369) # Use the min-height as a guide for html height
    st.markdown("---")

if show_technoserve:
    st.markdown("#### Technoserve's Presence")
    html(map_embed_codes["Technoserve's Presence"], height=330)
    st.markdown("---")

if show_action_needed:
    st.markdown("#### Action Needed (Please Verify Embed Code!)")
    html(map_embed_codes["Action Needed (Check Code)"], height=555)
    st.markdown("---")

# --- About Section ---
st.markdown("---")
st.subheader("About This Dashboard")
st.info("This prototype dashboard uses sample data for demonstration. In a full 'global food security index' application, this dataset would be significantly expanded and sourced from relevant nutritional and economic databases. The 'Protein Index' is a conceptual metric for this prototype.")
