import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load Protein Data (Sample Data) ---
# This function provides sample protein data for the dashboard.
# If you have actual protein data in a CSV or Excel file,
# you can modify this function to load it from your file.
@st.cache_data
def load_protein_data():
    # Sample data - replace with your actual data loading if available
    df = pd.DataFrame({
        'Food': ['Lentils', 'Chicken Breast', 'Tofu', 'Milk (Cow)', 'Egg (Large)', 'Salmon', 'Beef Steak', 'Quinoa'],
        'Protein Index': [78, 85, 92, 50, 88, 82, 75, 90],
        'Cost per gram protein': [0.4, 0.7, 0.5, 0.6, 0.45, 0.65, 0.9, 0.55],
        'Region': ['Asia', 'North America', 'Asia', 'Europe', 'North America', 'Europe', 'North America', 'South America']
    })
    # Ensure columns are numeric where expected
    df['Protein Index'] = pd.to_numeric(df['Protein Index'], errors='coerce')
    df['Cost per gram protein'] = pd.to_numeric(df['Cost per gram protein'], errors='coerce')
    df = df.dropna(subset=['Food', 'Protein Index', 'Cost per gram protein', 'Region'])
    return df

# --- Load GFSI Data from CSV File ---
@st.cache_data
def load_gfsi_data():
    try:
        # Read the GFSI scores from the provided CSV file.
        # Ensure 'GFSI_2022_All_Sheets_Clean.xlsx - tblScores_2022.csv' is in the same directory
        # as this app.py file, or provide the full path to the file.
        gfsi_df = pd.read_csv(
            "GFSI_2022_All_Sheets_Clean.xlsx - tblScores_2022.csv"
        )
        gfsi_df.columns = gfsi_df.columns.str.strip() # Clean column names

        # IMPORTANT: Rename columns to match the dashboard's expected names for GFSI.
        # You MUST VERIFY these 'Old Column Name': 'New Column Name' mappings
        # against the actual column headers in your 'tblScores_2022.csv' file.
        # Common names for country might be 'Country', 'Economy', 'ISO Code'.
        # Common names for score might be 'Score', 'Overall Score', '2022 Score'.
        gfsi_df = gfsi_df.rename(columns={
            'Country': 'Country', # Please verify this column name in your CSV
            'Score': 'GFSI Score' # Please verify this column name in your CSV
            # If your score column is named differently, e.g., 'Overall Score', change 'Score' to 'Overall Score'
        })

        required_gfsi_columns = ['Country', 'GFSI Score']
        for col in required_gfsi_columns:
            if col not in gfsi_df.columns:
                st.error(f"Error in GFSI data: Required column '{col}' not found after renaming. "
                         f"Please check your CSV file's column names and the renaming logic in app.py for GFSI data.")
                return pd.DataFrame(columns=required_gfsi_columns)

        # Convert GFSI Score to numeric, coercing errors to NaN
        gfsi_df['GFSI Score'] = pd.to_numeric(gfsi_df['GFSI Score'], errors='coerce')
        # Drop rows with missing values in critical columns
        gfsi_df = gfsi_df.dropna(subset=required_gfsi_columns)
        return gfsi_df
    except FileNotFoundError:
        st.error("Error: GFSI CSV file 'GFSI_2022_All_Sheets_Clean.xlsx - tblScores_2022.csv' not found. "
                 "Please ensure it's in the same directory as app.py.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred while loading GFSI data: {e}")
        return pd.DataFrame()

# Load data when the app starts
protein_data = load_protein_data()
gfsi_data = load_gfsi_data()

# --- Streamlit Page Configuration ---
st.set_page_config(layout="wide", page_title="Food Security Dashboards")

# --- Dashboard Title ---
st.title("Food Security & Protein Insights Dashboard")
st.markdown("Explore global food security trends and protein affordability.")

# --- Create Tabs ---
tab1, tab2 = st.tabs(["Protein Index & Affordability", "Global Food Security Index (GFSI)"])

# --- Tab 1: Protein Index & Affordability Dashboard ---
with tab1:
    st.header("Protein Index & Affordability")
    st.markdown("A prototype dashboard to identify cost-effective protein-rich foods based on expert research. **Note: Protein data is sample data.**")

    st.sidebar.header("Protein Filters")
    st.sidebar.markdown("Adjust the sliders and selections below to find the best protein sources.")

    # Protein Region Filter
    if 'Region' in protein_data.columns and not protein_data['Region'].empty:
        protein_regions = st.sidebar.multiselect(
            "Select Region(s) (Protein)",
            options=protein_data['Region'].unique(),
            default=list(protein_data['Region'].unique()), # Ensure default is a list
            help="Filter foods available in specific regions for protein analysis."
        )
    else:
        st.sidebar.warning("Protein Region data not available or empty. Cannot filter by region.")
        protein_regions = []

    # Protein Index Range Slider
    min_protein_index_data = int(protein_data['Protein Index'].min()) if 'Protein Index' in protein_data.columns and not protein_data['Protein Index'].empty else 0
    max_protein_index_data = int(protein_data['Protein Index'].max()) if 'Protein Index' in protein_data.columns and not protein_data['Protein Index'].empty else 100
    
    default_min_index_protein = min(70, max_protein_index_data) if max_protein_index_data >= 70 else min_protein_index_data
    default_max_index_protein = max(100, min_protein_index_data) if min_protein_index_data <= 100 else max_protein_index_data

    min_index, max_index = st.sidebar.slider(
        "Protein Index Range (Protein)",
        min_value=min_protein_index_data,
        max_value=max_protein_index_data,
        value=(default_min_index_protein, default_max_index_protein),
        step=5,
        help="Filter foods by their protein content efficiency (higher is better)."
    )

    # Max Cost per gram protein Slider
    min_cost_data = float(protein_data['Cost per gram protein'].min()) if 'Cost per gram protein' in protein_data.columns and not protein_data['Cost per gram protein'].empty else 0.1
    max_cost_data = float(protein_data['Cost per gram protein'].max()) if 'Cost per gram protein' in protein_data.columns and not protein_data['Cost per gram protein'].empty else 5.0

    default_max_cost_protein = min(1.0, max_cost_data) if max_cost_data >= 1.0 else max_cost_data

    max_cost = st.sidebar.slider(
        "Max Cost per gram protein (USD) (Protein)",
        min_value=min_cost_data,
        max_value=max_cost_data,
        value=default_max_cost_protein,
        step=0.05,
        help="Filter foods based on their affordability (lower cost is better)."
    )

    # Apply filters to protein data
    if not protein_data.empty:
        filtered_protein_data = protein_data[
            (protein_data['Region'].isin(protein_regions)) &
            (protein_data['Protein Index'].between(min_index, max_index)) &
            (protein_data['Cost per gram protein'] <= max_cost)
        ]
    else:
        filtered_protein_data = pd.DataFrame()

    st.subheader("Filtered Protein Sources Table")
    if filtered_protein_data.empty:
        st.warning("No protein sources match the selected filters or protein data could not be loaded. Please adjust your selections or check the data source.")
    else:
        st.dataframe(filtered_protein_data, use_container_width=True, height=250)

    st.subheader("Protein Index vs. Cost per gram protein")
    st.markdown("This chart visualizes the relationship between protein efficiency and cost. Look for items in the top-left quadrant (high protein index, low cost).")
    if not filtered_protein_data.empty and 'Food' in filtered_protein_data.columns:
        fig_protein = px.scatter(
            filtered_protein_data,
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
        fig_protein.update_layout(
            xaxis_title_standoff=10,
            yaxis_title_standoff=10,
            legend_title="Food Source",
            hovermode="closest"
        )
        st.plotly_chart(fig_protein, use_container_width=True)
    else:
        st.info("No data to display in the protein chart. Adjust filters to see results.")

    st.subheader("Key Insights (Protein)")
    if filtered_protein_data.empty:
        st.info("No insights available for protein as no data matches the current filters.")
    else:
        total_foods = len(protein_data)
        displayed_foods = len(filtered_protein_data)

        st.markdown(f"**{displayed_foods}** out of **{total_foods}** protein sources are currently displayed based on your filters.")
        
        if not filtered_protein_data['Protein Index'].empty:
            st.markdown(f"**Average Protein Index** of filtered foods: **{filtered_protein_data['Protein Index'].mean():.2f}**")
        else:
            st.markdown("Average Protein Index: N/A (no data)")

        if not filtered_protein_data['Cost per gram protein'].empty:
            st.markdown(f"**Average Cost per gram protein** of filtered foods: **${filtered_protein_data['Cost per gram protein'].mean():.2f}**")
        else:
            st.markdown("Average Cost per gram protein: N/A (no data)")

        if not filtered_protein_data.empty and 'Cost per gram protein' in filtered_protein_data.columns and not filtered_protein_data['Cost per gram protein'].empty:
            most_cost_effective = filtered_protein_data.loc[filtered_protein_data['Cost per gram protein'].idxmin()]
            st.markdown(f"The most **cost-effective** protein source in the filtered list is **{most_cost_effective['Food']}** (Protein Index: {most_cost_effective['Protein Index']}, Cost: ${most_cost_effective['Cost per gram protein']:.2f}/g protein).")
        else:
            st.markdown("Most cost-effective protein source: N/A (no data)")

        if not filtered_protein_data.empty and 'Protein Index' in filtered_protein_data.columns and not filtered_protein_data['Protein Index'].empty:
            highest_protein_index = filtered_protein_data.loc[filtered_protein_data['Protein Index'].idxmax()]
            st.markdown(f"The protein source with the **highest Protein Index** is **{highest_protein_index['Food']}** (Protein Index: {highest_protein_index['Protein Index']}, Cost: ${highest_protein_index['Cost per gram protein']:.2f}/g protein).")
        else:
            st.markdown("Highest protein index food: N/A (no data)")

# --- Tab 2: Global Food Security Index (GFSI) Dashboard ---
with tab2:
    st.header("Global Food Security Index (GFSI)")
    st.markdown("Visualize and filter countries based on their GFSI scores.")

    st.sidebar.header("GFSI Filters")
    st.sidebar.markdown("Adjust the sliders and selections below to explore GFSI data.")

    # GFSI Country Filter
    if 'Country' in gfsi_data.columns and not gfsi_data['Country'].empty:
        gfsi_countries = st.sidebar.multiselect(
            "Select Country(ies) (GFSI)",
            options=gfsi_data['Country'].unique(),
            default=list(gfsi_data['Country'].unique()), # Ensure default is a list
            help="Filter countries for GFSI analysis."
        )
    else:
        st.sidebar.warning("GFSI Country data not available or empty. Cannot filter by country.")
        gfsi_countries = []

    # GFSI Score Range Slider
    min_gfsi_score_data = int(gfsi_data['GFSI Score'].min()) if 'GFSI Score' in gfsi_data.columns and not gfsi_data['GFSI Score'].empty else 0
    max_gfsi_score_data = int(gfsi_data['GFSI Score'].max()) if 'GFSI Score' in gfsi_data.columns and not gfsi_data['GFSI Score'].empty else 100

    min_gfsi_score, max_gfsi_score = st.sidebar.slider(
        "GFSI Score Range (GFSI)",
        min_value=min_gfsi_score_data,
        max_value=max_gfsi_score_data,
        value=(min_gfsi_score_data, max_gfsi_score_data),
        step=1,
        help="Filter countries by their GFSI score (higher is better)."
    )

    # Apply filters to GFSI data
    if not gfsi_data.empty:
        filtered_gfsi_data = gfsi_data[
            (gfsi_data['Country'].isin(gfsi_countries)) &
            (gfsi_data['GFSI Score'].between(min_gfsi_score, max_gfsi_score))
        ]
    else:
        filtered_gfsi_data = pd.DataFrame()

    st.subheader("Filtered GFSI Data Table")
    if filtered_gfsi_data.empty:
        st.warning("No GFSI data matches the selected filters or GFSI data could not be loaded. Please adjust your selections or check the Excel file.")
    else:
        st.dataframe(filtered_gfsi_data, use_container_width=True, height=300)

    st.subheader("Global Food Security Index Map")
    st.markdown("This map visualizes GFSI scores by country. Higher scores indicate better food security.")

    if not filtered_gfsi_data.empty and 'Country' in filtered_gfsi_data.columns and 'GFSI Score' in filtered_gfsi_data.columns:
        fig_gfsi = px.choropleth(
            filtered_gfsi_data,
            locations="Country",
            locationmode="country names",
            color="GFSI Score",
            hover_name="Country",
            color_continuous_scale=px.colors.sequential.Plasma,
            title="Global Food Security Index by Country",
            labels={'GFSI Score': 'GFSI Score'},
            height=600
        )
        fig_gfsi.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            )
        )
        st.plotly_chart(fig_gfsi, use_container_width=True)
    else:
        st.info("No data to display in the GFSI map. Adjust filters to see results.")

    st.subheader("Key Insights (GFSI)")
    if filtered_gfsi_data.empty:
        st.info("No insights available for GFSI as no data matches the current filters.")
    else:
        total_gfsi_countries = len(gfsi_data)
        displayed_gfsi_countries = len(filtered_gfsi_data)

        st.markdown(f"**{displayed_gfsi_countries}** out of **{total_gfsi_countries}** countries are currently displayed based on your GFSI filters.")
        
        if not filtered_gfsi_data['GFSI Score'].empty:
            st.markdown(f"**Average GFSI Score** of filtered countries: **{filtered_gfsi_data['GFSI Score'].mean():.2f}**")
        else:
            st.markdown("Average GFSI Score: N/A (no data)")

        if not filtered_gfsi_data['GFSI Score'].empty and filtered_gfsi_data['GFSI Score'].nunique() > 0:
            highest_score_country = filtered_gfsi_data.loc[filtered_gfsi_data['GFSI Score'].idxmax()]
            st.markdown(f"Country with the **highest GFSI Score**: **{highest_score_country['Country']}** ({highest_score_country['GFSI Score']:.2f})")

            lowest_score_country = filtered_gfsi_data.loc[filtered_gfsi_data['GFSI Score'].idxmin()]
            st.markdown(f"Country with the **lowest GFSI Score**: **{lowest_score_country['Country']}** ({lowest_score_country['GFSI Score']:.2f})")
        else:
            st.markdown("Cannot determine highest/lowest GFSI score (insufficient data or all scores are identical).")
        
