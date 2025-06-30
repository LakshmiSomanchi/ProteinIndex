# proteinindex.py (or app.py)

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.components.v1 import html # Import html component for embedding

# --- Sample Data (from your original dashboard) ---
data = pd.DataFrame({
    'Food': ['Lentils', 'Chicken', 'Soy', 'Milk', 'Egg', 'Fish', 'Beef', 'Quinoa'],
    'Protein Index': [78, 85, 92, 50, 88, 82, 75, 90],
    'Cost per gram protein': [0.4, 0.7, 0.5, 0.6, 0.45, 0.65, 0.9, 0.55],
    'Region': ['Asia', 'US', 'Asia', 'Europe', 'US', 'Europe', 'US', 'Asia']
})

# --- Configuration for all CSV Sheets ---
# This dictionary maps a clean tab name to its file path and skiprows value.
# Ensure these CSV files are in the same directory as this Python script
# when deploying to GitHub/Streamlit Cloud.
csv_sheets_info = {
    "Indicators": {"path": "TNS_USSEC_Protein Nutrition Score_Working Sheet_Ver1.0.xlsx - Indicators.csv", "skiprows": 0},
    "Data Sources": {"path": "TNS_USSEC_Protein Nutrition Score_Working Sheet_Ver1.0.xlsx - Data Sources.csv", "skiprows": 0},
    "US Soy Export": {"path": "TNS_USSEC_Protein Nutrition Score_Working Sheet_Ver1.0.xlsx - US Soy Export.csv", "skiprows": 1},
    "Global Data": {"path": "TNS_USSEC_Protein Nutrition Score_Working Sheet_Ver1.0.xlsx - Global Data.csv", "skiprows": 1},
    "Regions Countries": {"path": "TNS_USSEC_Protein Nutrition Score_Working Sheet_Ver1.0.xlsx - Regions Countries.csv", "skiprows": 0},
    "Organogram": {"path": "TNS_USSEC_Protein Nutrition Score_Working Sheet_Ver1.0.xlsx - Organogram.csv", "skiprows": 0},
    "TNS Programs": {"path": "TNS_USSEC_Protein Nutrition Score_Working Sheet_Ver1.0.xlsx - TNS Programs.csv", "skiprows": 1},
    "Work Plan Archive": {"path": "TNS_USSEC_Protein Nutrition Score_Working Sheet_Ver1.0.xlsx - Work Plan archive.csv", "skiprows": 0},
    "Summary and Expenses": {"path": "TNS_USSEC_Protein Nutrition Score_Working Sheet_Ver1.0.xlsx - Summary and Expenses.csv", "skiprows": 2},
    "Work Plan": {"path": "TNS_USSEC_Protein Nutrition Score_Working Sheet_Ver1.0.xlsx - Work Plan.csv", "skiprows": 2},
    "Result Framework": {"path": "TNS_USSEC_Protein Nutrition Score_Working Sheet_Ver1.0.xlsx - Result Framework.csv", "skiprows": 2},
    "Logframe": {"path": "TNS_USSEC_Protein Nutrition Score_Working Sheet_Ver1.0.xlsx - Logframe.csv", "skiprows": 1},
}

# --- Load all CSVs into a dictionary of DataFrames ---
loaded_dfs = {}
for tab_name, info in csv_sheets_info.items():
    try:
        # skiprows + 1 because pandas skiprows is 0-indexed for number of rows *to skip*
        # if estimatedRowsAboveHeader is 1, it means the header is on the 2nd row (index 1), so skip 1 row.
        # if estimatedRowsAboveHeader is 2, it means the header is on the 3rd row (index 2), so skip 2 rows.
        # So, skiprows = estimatedRowsAboveHeader
        loaded_dfs[tab_name] = pd.read_csv(info["path"], skiprows=info["skiprows"])
        st.cache_data(pd.read_csv)(info["path"], skiprows=info["skiprows"]) # Cache the data loading
    except FileNotFoundError:
        st.error(f"Error: Could not find file '{info['path']}'. Please ensure it's in the same directory.")
        loaded_dfs[tab_name] = pd.DataFrame({"Error": [f"File not found: {info['path']}"]})
    except Exception as e:
        st.error(f"Error loading '{info['path']}': {e}")
        loaded_dfs[tab_name] = pd.DataFrame({"Error": [f"Error loading data: {e}"]})


# --- Streamlit Page Configuration ---
st.set_page_config(layout="wide", page_title="Protein & Food Security Dashboard")

# --- Dashboard Title ---
st.title("Protein Index & Global Food Security Dashboard")
st.markdown("A comprehensive dashboard for protein analysis, global food security visualizations, and detailed data insights.")

# --- Define the tabs ---
# Main dashboard tabs first, then dynamically add tabs for each loaded CSV sheet
tab_names = ["Protein Dashboard", "Global Maps"] + list(csv_sheets_info.keys())
tabs = st.tabs(tab_names)

# --- Content for "Protein Dashboard" Tab ---
with tabs[0]:
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

# --- Content for "Global Maps" Tab ---
with tabs[1]:
    st.header("Global Food Security Visualizations")
    st.markdown("Select the maps below to view different aspects of global food security and relevant initiatives.")

    # Define the HTML embed codes for each map
    map_embed_codes = {
        "GFSI World Hunger Data": """
        <div style="min-height:369px; width:100%" id="datawrapper-vis-d0yRp"><script type="text/javascript" defer src="https://datawrapper.dwcdn.net/d0yRp/embed.js" charset="utf-8" data-target="#datawrapper-vis-d0yRp"></script><noscript><img src="https://datawrapper.dwcdn.net/d0yRp/full.png" alt="" /></noscript></div>
        """,
        "Technoserve's Presence": """
        <div style="min-height:357px; width:100%" id="datawrapper-vis-pf5wv"><script type="text/javascript" defer src="https://datawrapper.dwcdn.net/pf5wv/embed.js" charset="utf-8" data-target="#datawrapper-vis-pf5wv"></script><noscript><img src="https://datawrapper.dwcdn.net/pf5wv/full.png" alt="" /></noscript></div>
        """,
        "Action Needed (Check Code)": """
        <div style="min-height:555px; width:100%" id="datawrapper-vis-pf5wv"><script type="text/javascript" defer src="https://datawrapper.dwcdn.net/pf5wv/embed.js" charset="utf-8" data-target="#datawrapper-vis-pf5wv"></script><noscript><img src="https://datawrapper.dwcdn.net/pf5wv/full.png" alt="" /></noscript></div>
        """
    }

    # Add checkboxes for map selection in the sidebar (or directly in the tab if preferred)
    st.sidebar.header("Map Display Options")
    show_gfsi = st.sidebar.checkbox("Show GFSI World Hunger Data Map", value=True) # Show by default
    show_technoserve = st.sidebar.checkbox("Show Technoserve's Presence Map")
    show_action_needed = st.sidebar.checkbox("Show Action Needed Map (Verify Code)", help="Please verify this map's embed code if it's different from Technoserve's.")

    # Display maps based on checkbox selection
    if show_gfsi:
        st.markdown("#### GFSI World Hunger Data")
        html(map_embed_codes["GFSI World Hunger Data"], height=369)
        st.markdown("---")

    if show_technoserve:
        st.markdown("#### Technoserve's Presence")
        html(map_embed_codes["Technoserve's Presence"], height=357)
        st.markdown("---")

    if show_action_needed:
        st.markdown("#### Action Needed (Please Verify Embed Code!)")
        html(map_embed_codes["Action Needed (Check Code)"], height=555)
        st.markdown("---")

# --- Content for Data Sheet Tabs (loop through loaded_dfs) ---
# Start from index 2 because tabs[0] is "Protein Dashboard" and tabs[1] is "Global Maps"
for i, tab_name in enumerate(list(csv_sheets_info.keys())):
    with tabs[i + 2]: # Offset by 2 for the first two custom tabs
        st.header(f"Data from '{tab_name}' Sheet")
        if not loaded_dfs[tab_name].empty and "Error" not in loaded_dfs[tab_name].columns:
            st.dataframe(loaded_dfs[tab_name], use_container_width=True)
            st.download_button(
                label=f"Download {tab_name} Data as CSV",
                data=loaded_dfs[tab_name].to_csv(index=False).encode('utf-8'),
                file_name=f'{tab_name.lower().replace(" ", "_")}_data.csv',
                mime='text/csv',
                help=f"Download the data from the '{tab_name}' sheet."
            )
        else:
            st.warning(f"Could not load data for '{tab_name}'. Check file path and content.")
            st.dataframe(loaded_dfs[tab_name]) # Display error dataframe


# --- About Section (remains at the bottom, outside any specific tab) ---
st.markdown("---")
st.subheader("About This Dashboard")
st.info("This prototype dashboard combines protein index analysis with interactive global food security visualizations and presents raw data from various sheets of the 'TNS_USSEC_Protein Nutrition Score' Excel file. The maps are static embeds for demonstration; for a full application, detailed geographical and socio-economic data would be required. The 'Protein Index' is a conceptual metric for this prototype.")
