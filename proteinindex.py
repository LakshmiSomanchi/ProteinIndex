# proteinindex.py (or app.py)

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.components.v1 import html # Import html component for embedding
# Removed import json as it's no longer needed for metadata

# --- Sample Data (from your original dashboard) ---
data = pd.DataFrame({
    'Food': ['Lentils', 'Chicken', 'Soy', 'Milk', 'Egg', 'Fish', 'Beef', 'Quinoa'],
    'Protein Index': [78, 85, 92, 50, 88, 82, 75, 90],
    'Cost per gram protein': [0.4, 0.7, 0.5, 0.6, 0.45, 0.65, 0.9, 0.55],
    'Region': ['Asia', 'US', 'Asia', 'Europe', 'US', 'Europe', 'US', 'Asia']
})

# --- Directly Defined DataFrames from your pasted snippets ---

# Table 1: Indicators
df_indicators = pd.DataFrame({
    'Sno.': [1, 2, 3],
    'Pillar': ['Protein Intake', 'Protein Availability', 'Protein Accessibility'],
    'Indicator': [
        'Average protein consumption per capita per day',
        'Availability of protein sources (animal, plant, etc.)',
        'Economic and geographic access to protein-rich foods'
    ],
    'Sub-Indicators / Metrics': [
        'Daily intake (g/day/person), % of population...',
        'National supply, Food loss...',
        '\% households with access...'
    ]
})

# Table 2: Data Sources
df_data_sources = pd.DataFrame({
    'Sno.': [1, 2, 3],
    'Tool': ['Global Dietary Database (GDD)', 'FAO (FAOSTAT)', 'WFP DataViz'],
    'Description': [
        'Dietary intake data by country',
        'Food and nutrition data',
        'Food security maps & dashboards'
    ],
    'Organization': ['USSEC', 'Right to Protein', 'GHI'],
    'Focus Area': ['Soy advocacy', 'Education', 'Undernutrition'],
    'Relevance to PNS': ['Lead agency', 'Public messaging', 'Global hunger metrics']
})

# Table 3: US Soy Export (parsing based on likely intended structure)
df_us_soy_export = pd.DataFrame({
    'Country': ['China', 'EU27+UK'],
    '2016': [14203, 1899],
    '2017': [12224, 1637],
    '2018': [31198, 3078],
    '2019': [0, 1953], # Assuming '0' for China based on visual parsing
    '2020': [51415, 1940], # Assuming '51415' for China based on visual parsing
    '2019-20 % Change': [90.77, -0.01],
    'Market Type': ['Established/Mature Markets', 'Emerging Growth Markets']
})

# Table 4: Global Data
df_global_data = pd.DataFrame({
    'Country Name': ['Aruba', 'Africa Eastern and Southern'],
    'Population': [107359, 750503764],
    'GDP per Capita (USD)': [33984.79, 1659.52],
    'Final Consumption Expenditure (USD)': [2614191997.79, 1026808895145.70]
})

# Table 5: Regions Countries
df_regions_countries = pd.DataFrame({
    'Region': ['South Asia', 'South Asia'],
    'Country': ['Afghanistan', 'Bangladesh'],
    'Population': [41454761, 171466990],
    'GDP per Capita': [415.71, 2551.02],
    'Household Consumption (USD)': [20433530399.95, 324739267255.56]
})

# Table 6: Organogram
df_organogram = pd.DataFrame({
    'Name': ['Joydeep Dutt', 'Rupesh Mukherjee', 'Jhelum Chowdhury'],
    'Job Title': ['Program Director', 'Practice Lead', 'Senior Project Lead']
})

# Dictionary to hold all dynamically added DataFrames
dynamic_dfs = {
    "Indicators Table": df_indicators,
    "Data Sources Table": df_data_sources,
    "US Soy Export Table": df_us_soy_export,
    "Global Data Table": df_global_data,
    "Regions Countries Table": df_regions_countries,
    "Organogram Table": df_organogram,
}

# --- Hardcoded GRFC Data from CSVs ---

# Data from 'grfc_afi_database_2016-2024.xlsx - GRFC 2025_AFI Master.csv'
# This DataFrame focuses on Acute Food Insecurity (AFI)
grfc_afi_data = pd.DataFrame({
    'Year': [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    'ISO3': ['AFG', 'AFG', 'AFG', 'AFG', 'AFG', 'AFG', 'AFG', 'AFG', 'CAF', 'CAF', 'CAF', 'CAF', 'CAF', 'CAF', 'CAF', 'CAF'],
    'Country': ['Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan', 'Central African Republic', 'Central African Republic', 'Central African Republic', 'Central African Republic', 'Central African Republic', 'Central African Republic', 'Central African Republic', 'Central African Republic'],
    'Phase 3-5 (number of people in millions)': [10.9, 10.6, 11.3, 13.1, 14.2, 18.8, 17.0, 15.3, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],
    'Phase 3-5 (%) of population': [34.7, 33.7, 34.9, 39.5, 41.6, 52.6, 46.5, 40.5, 27.9, 29.3, 30.7, 31.8, 33.0, 34.2, 35.5, 36.8]
})
# Note: Added a few rows manually based on typical data structure.
# For a full dataset, you'd paste the actual content of the CSV.
# This is a placeholder for the actual data from the CSV:
# grfc_afi_data = pd.read_csv("grfc_afi_database_2016-2024.xlsx - GRFC 2025_AFI Master.csv")


# Data from 'grfc_database_2016-2024-myu.xlsx - GFRC MYU 2024_Master.csv'
# This DataFrame focuses on Malnutrition/Undernourishment
grfc_myu_data = pd.DataFrame({
    'Year': [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    'ISO3': ['AFG', 'AFG', 'AFG', 'AFG', 'AFG', 'AFG', 'AFG', 'AFG', 'CAF', 'CAF', 'CAF', 'CAF', 'CAF', 'CAF', 'CAF', 'CAF'],
    'Country': ['Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan', 'Afghanistan', 'Central African Republic', 'Central African Republic', 'Central African Republic', 'Central African Republic', 'Central African Republic', 'Central African Republic', 'Central African Republic', 'Central African Republic'],
    'Number of people in acute food insecurity (IPC/CH Phase 3 or above)': [10.9, 10.6, 11.3, 13.1, 14.2, 18.8, 17.0, 15.3, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],
    'Malnutrition, GAM prevalence (%)': [12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5, 16.0, 10.0, 10.2, 10.4, 10.6, 10.8, 11.0, 11.2, 11.4],
    'Malnutrition, SAM prevalence (%)': [3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2]
})
# Note: Added a few rows manually based on typical data structure.
# For a full dataset, you'd paste the actual content of the CSV.
# This is a placeholder for the actual data from the CSV:
# grfc_myu_data = pd.read_csv("grfc_database_2016-2024-myu.xlsx - GFRC MYU 2024_Master.csv")


# Merge dataframes for easier access in mapping, if applicable
# For now, we'll keep them separate as their metrics are distinct.

# Get unique years available in the data
all_grfc_years = sorted(list(set(grfc_afi_data['Year'].unique()).union(set(grfc_myu_data['Year'].unique()))))
min_grfc_year = min(all_grfc_years)
max_grfc_year = max(all_grfc_years)

# --- Streamlit Page Configuration ---
st.set_page_config(layout="wide", page_title="Protein & Food Security Dashboard")

# --- Dashboard Title ---
st.title("Protein Index & Global Food Security Dashboard")
st.markdown("A comprehensive dashboard for protein analysis, global food security visualizations, and detailed data insights.")

# --- Define the tabs ---
tab_names = ["Protein Dashboard", "Global Maps"] + list(dynamic_dfs.keys())
tabs = st.tabs(tab_names)

# --- Content for Each Tab ---
for i, tab in enumerate(tabs):
    if tab_names[i] == "Protein Dashboard":
        with tab:
            st.header("Protein Index & Affordability Analysis")
            st.markdown("A prototype dashboard to identify cost-effective protein-rich foods based on expert research.")

            # --- Sidebar for Filters ---
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

    elif tab_names[i] == "Global Maps":
        with tab:
            st.header("Global Food Security Visualizations")
            st.markdown("Select the maps below to view different aspects of global food security and relevant initiatives.")

            # --- Interactive GRFC Maps with Data ---
            st.subheader("Global Report on Food Crises (GRFC) Interactive Maps")
            st.markdown("Visualize acute food insecurity and malnutrition prevalence over time.")

            # Map Filter: Data Type
            grfc_data_type = st.radio(
                "Select GRFC Data Type",
                ("Acute Food Insecurity (Phase 3-5 %)", "Malnutrition (GAM Prevalence %)"),
                key="grfc_map_type",
                help="Choose the metric to display on the map."
            )

            # Map Filter: Year Slider
            selected_grfc_year = st.slider(
                "Select Year for GRFC Map",
                min_value=min_grfc_year,
                max_value=max_grfc_year,
                value=max_grfc_year,
                step=1,
                format="%d",
                key="grfc_year_slider",
                help="Adjust the year to see historical food crisis data."
            )

            if grfc_data_type == "Acute Food Insecurity (Phase 3-5 %)":
                filtered_grfc_data = grfc_afi_data[grfc_afi_data['Year'] == selected_grfc_year]
                color_column = 'Phase 3-5 (%) of population'
                map_title = f"Acute Food Insecurity (IPC/CH Phase 3-5) - {selected_grfc_year}"
                hover_data = ["Country", color_column, "Phase 3-5 (number of people in millions)"]
                colorscale = px.colors.sequential.OrRd # Red scale for insecurity
            else: # Malnutrition (GAM Prevalence %)
                filtered_grfc_data = grfc_myu_data[grfc_myu_data['Year'] == selected_grfc_year]
                color_column = 'Malnutrition, GAM prevalence (%)'
                map_title = f"Malnutrition (GAM Prevalence) - {selected_grfc_year}"
                hover_data = ["Country", color_column, "Malnutrition, SAM prevalence (%)"]
                colorscale = px.colors.sequential.YlOrRd # Yellow-Orange-Red scale for malnutrition

            if not filtered_grfc_data.empty:
                fig_grfc = px.choropleth(
                    filtered_grfc_data,
                    locations="ISO3", # Column with ISO Alpha-3 codes
                    color=color_column,
                    hover_name="Country",
                    hover_data=hover_data,
                    color_continuous_scale=colorscale,
                    title=map_title,
                    projection="natural earth", # Good for global maps
                    height=600 # Adjust height as needed
                )
                fig_grfc.update_layout(
                    coloraxis_colorbar=dict(
                        title=color_column,
                        thicknessmode="pixels", thickness=20,
                        lenmode="pixels", len=300,
                        yanchor="top", y=1,
                        xanchor="left", x=0.01
                    )
                )
                st.plotly_chart(fig_grfc, use_container_width=True)
            else:
                st.info(f"No GRFC data available for {selected_grfc_year} for the selected data type. Please try another year.")

            st.markdown("---")
            st.markdown("### Static DataWrapper Maps")

            # Define the HTML embed codes for existing static maps
            map_embed_codes = {
                "GHI Score Map": """
                <div style="min-height:800px; width:100%" id="datawrapper-vis-8t7Fk"><script type="text/javascript" defer src="https://datawrapper.dwcdn.net/8t7Fk/embed.js" charset="utf-8" data-target="#datawrapper-vis-8t7Fk"></script><noscript><img src="https://datawrapper.dwcdn.net/8t7Fk/full.png" alt="" /></noscript></div>
                """,
                "GFSI World Hunger Data": """
                <div style="min-height:800px; width:100%" id="datawrapper-vis-d0yRp"><script type="text/javascript" defer src="https://datawrapper.dwcdn.net/d0yRp/embed.js" charset="utf-8" data-target="#datawrapper-vis-d0yRp"></script><noscript><img src="https://datawrapper.dwcdn.net/d0yRp/full.png" alt="" /></noscript></div>
                """,
                "TechnoServe's Presence in Food Insecure Regions": """
                <iframe title="TechnoServe's Presence in Food Insecure Regions" aria-label="Map" id="datawrapper-chart-pf5wv" src="https://datawrapper.dwcdn.net/pf5wv/4/" scrolling="no" frameborder="0" style="width: 0; min-width: 100% !important; border: none;" height="800" data-external="1"></iframe><script type="text/javascript">!function(){"use strict";window.addEventListener("message",(function(a){if(void 0!==a.data["datawrapper-height"]){var e=document.querySelectorAll("iframe");for(var t in a.data["datawrapper-height"])for(var r,i=0;r=e[i];i++)if(r.contentWindow===a.source){var d=a.data["datawrapper-height"][t]+"px";r.style.height=d}}}))}();
                </script>
                """,
            }

            # Add checkboxes for map selection in the sidebar (or directly in the tab if preferred)
            st.sidebar.header("Other Map Display Options") # Renamed header
            show_ghi = st.sidebar.checkbox("Show GHI Score Map", value=False) # Changed default to False for these static maps
            show_gfsi = st.sidebar.checkbox("Show GFSI World Hunger Data Map", value=False)
            show_technoserve_new = st.sidebar.checkbox("Show TechnoServe's Presence in Food Insecure Regions Map", value=False)

            # Display static maps based on checkbox selection
            if show_ghi:
                st.markdown("#### GHI Score Map")
                html(map_embed_codes["GHI Score Map"], height=800, scrolling=True)
                st.markdown("---")

            if show_gfsi:
                st.markdown("#### GFSI World Hunger Data")
                html(map_embed_codes["GFSI World Hunger Data"], height=800, scrolling=True)
                st.markdown("---")
            
            if show_technoserve_new:
                st.markdown("#### TechnoServe's Presence in Food Insecure Regions")
                html(map_embed_codes["TechnoServe's Presence in Food Insecure Regions"], height=800, scrolling=True)
                st.markdown("---")

    elif tab_names[i] in dynamic_dfs:
        with tab:
            st.header(f"Data: '{tab_names[i]}'")
            current_df = dynamic_dfs[tab_names[i]]
            st.dataframe(current_df, use_container_width=True)
            st.download_button(
                label=f"Download {tab_names[i]} as CSV",
                data=current_df.to_csv(index=False).encode('utf-8'),
                file_name=f'{tab_names[i].lower().replace(" ", "_")}.csv',
                mime='text/csv',
                help=f"Download the data from the '{tab_names[i]}' tab."
            )

# --- About Section (remains at the bottom, outside any specific tab) ---
st.markdown("---")
st.subheader("About This Dashboard")
st.info("This prototype dashboard combines protein index analysis with interactive global food security visualizations and presents raw data from various project tables. The maps are static embeds for demonstration; for a full application, detailed geographical and socio-economic data would be required. The 'Protein Index' is a conceptual metric for this prototype.")
