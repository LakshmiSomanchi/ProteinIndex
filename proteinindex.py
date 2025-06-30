# proteinindex.py (or app.py)

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.components.v1 import html
import folium
from streamlit_folium import st_folium # Import the Streamlit Folium component

# --- Sample Data (from your original dashboard) ---
data = pd.DataFrame({
    'Food': ['Lentils', 'Chicken', 'Soy', 'Milk', 'Egg', 'Fish', 'Beef', 'Quinoa'],
    'Protein Index': [78, 85, 92, 50, 88, 82, 75, 90],
    'Cost per gram protein': [0.4, 0.7, 0.5, 0.6, 0.45, 0.65, 0.9, 0.55],
    'Region': ['Asia', 'US', 'Asia', 'Europe', 'US', 'Europe', 'US', 'Asia']
})

# --- Placeholder Data for Maps (YOU NEED TO REPLACE THIS WITH YOUR REAL DATA) ---
# Assume ISO-alpha3 country codes for joining with GeoJSON
# Placeholder GFSI data (replace with your actual data and values)
# Example: Higher value means worse food security
gfsi_data = pd.DataFrame({
    'country_code': ['USA', 'CHN', 'IND', 'DEU', 'FRA', 'GBR', 'BRA', 'NGA'],
    'gfsi_score': [20, 50, 70, 15, 25, 18, 40, 85] # Example scores
})

# Placeholder Technoserve Presence data (replace with your actual data)
# Example: 1 for presence, 0 for no presence
technoserve_presence_data = pd.DataFrame({
    'country_code': ['IND', 'NGA', 'BRA', 'KEN', 'ETH'], # Example countries
    'presence': [1, 1, 1, 1, 1]
})

# Placeholder Action Needed data (replace with your actual data)
# Example: Higher value means more urgent action needed
action_needed_data = pd.DataFrame({
    'country_code': ['IND', 'NGA', 'ETH', 'COD', 'SDN'], # Example countries
    'action_urgency': [3, 4, 3, 5, 5]
})

# --- Local GeoJSON File Path ---
# IMPORTANT: Ensure 'countries_110m.geojson' is in the same directory as this script.
local_geojson_path = "countries_110m.geojson"

# --- Streamlit Page Configuration ---
st.set_page_config(layout="wide", page_title="Protein Index & Food Security Dashboard")

# --- Dashboard Title ---
st.title("Protein Index & Global Food Security Dashboard")
st.markdown("A prototype dashboard to identify cost-effective protein-rich foods and visualize global food security data.")

# --- Sidebar for Filters (from previous code) ---
st.sidebar.header("Protein Source Filter Options")
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


# --- Integrated Map Section with Folium ---
st.subheader("Interactive Global Food Security Map")
st.markdown("Use the layer control icon (top right of the map) to toggle different data layers.")

# Create a Folium map object, centered and zoomed appropriately
m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodbpositron") # Centered near equator, world view

# Layer 1: GFSI World Hunger Data (Choropleth)
folium.Choropleth(
    geo_data=local_geojson_path, # Using local file path
    name="GFSI World Hunger Data",
    data=gfsi_data,
    columns=['country_code', 'gfsi_score'],
    key_on="feature.properties.ISO_A3",
    fill_color='YlOrRd', # Yellow-Orange-Red for higher scores (worse)
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='GFSI Score (Higher = More Hunger)',
    highlight=True, # Highlight country on hover
    overlay=True # Essential for layer control
).add_to(m)

# Layer 2: Technoserve's Presence (Example: color countries with presence)
folium.Choropleth(
    geo_data=local_geojson_path, # Using local file path
    name="Technoserve's Presence",
    data=technoserve_presence_data,
    columns=['country_code', 'presence'],
    key_on="feature.properties.ISO_A3",
    fill_color='GnBu', # Green-Blue for presence
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Technoserve Presence (1=Yes)',
    highlight=True,
    overlay=True, # Essential for layer control
    show=False # Start with this layer off
).add_to(m)

# Layer 3: Action Needed (Example: color countries by urgency)
folium.Choropleth(
    geo_data=local_geojson_path, # Using local file path
    name="Action Needed",
    data=action_needed_data,
    columns=['country_code', 'action_urgency'],
    key_on="feature.properties.ISO_A3",
    fill_color='OrRd', # Orange-Red for urgency
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Action Urgency (Higher = More Urgent)',
    highlight=True,
    overlay=True, # Essential for layer control
    show=False # Start with this layer off
).add_to(m)


# Add a LayerControl to the map
# This creates the legend with checkboxes
folium.LayerControl().add_to(m)

# Display the Folium map in Streamlit
st_folium(m, width=900, height=500) # Adjust width/height as needed

# --- About Section ---
st.markdown("---")
st.subheader("About This Dashboard")
st.info("This prototype dashboard combines protein index analysis with interactive global food security visualizations. The map data is illustrative placeholders; for a full application, detailed geographical and socio-economic data would be required. The 'Protein Index' is a conceptual metric for this prototype.")
