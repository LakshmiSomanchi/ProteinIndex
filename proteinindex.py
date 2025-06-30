import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load Protein Data from Excel File ---
# Use st.cache_data to cache the data loading,
# so it only runs once when the app starts or the file changes.
@st.cache_data
def load_protein_data():
    try:
        # Read the Excel file.
        # Ensure 'Economist_Impact_GFSI_2022_Model_Sep_2022 (1).xlsm' is in the same directory
        # as this app.py file, or provide the full path to the file.
        # sheet_name=0 reads the first sheet. Change this if your data is on a different sheet
        # (e.g., sheet_name="YourProteinDataSheetName").
        df = pd.read_excel(
            "Economist_Impact_GFSI_2022_Model_Sep_2022 (1).xlsm",
            sheet_name=0 # Assuming protein data is on the first sheet
        )
        
        # Strip whitespace from column names to ensure clean matching
        df.columns = df.columns.str.strip()

        # IMPORTANT: Rename columns to match the dashboard's expected names for protein data.
        # You MUST verify these 'Old Column Name': 'New Column Name' mappings
        # against the actual column headers in your Excel file for protein data.
        # If your Excel file uses different names, update these mappings accordingly.
        df = df.rename(columns={
            'Food Name': 'Food', # Example: Replace 'Food Name' with your actual food column
            'Protein Efficiency Index': 'Protein Index', # Example: Replace with your actual protein index column
            'Cost USD/g protein': 'Cost per gram protein', # Example: Replace with your actual cost column
            'Geographic Region': 'Region' # Example: Replace with your actual region column
        })

        # Ensure required columns exist after renaming
        required_columns = ['Food', 'Protein Index', 'Cost per gram protein', 'Region']
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Error in protein data: Required column '{col}' not found after renaming. "
                         f"Please check your Excel file's column names and the renaming logic in app.py for protein data.")
                return pd.DataFrame(columns=required_columns) # Return empty DataFrame on error

        # Convert 'Protein Index' and 'Cost per gram protein' to numeric, coercing errors
        df['Protein Index'] = pd.to_numeric(df['Protein Index'], errors='coerce')
        df['Cost per gram protein'] = pd.to_numeric(df['Cost per gram protein'], errors='coerce')

        # Drop rows where critical columns have missing (NaN) values after conversion
        df = df.dropna(subset=required_columns)
        
        return df
    except FileNotFoundError:
        st.error("Error: Excel file 'Economist_Impact_GFSI_2022_Model_Sep_2022 (1).xlsm' not found. "
                 "Please ensure it's in the same directory as app.py.")
        return pd.DataFrame() # Return an empty DataFrame if file not found
    except Exception as e:
        st.error(f"An error occurred while loading protein data: {e}")
        return pd.DataFrame() # Return an empty DataFrame on other errors

# --- Load GFSI Data from Excel File ---
@st.cache_data
def load_gfsi_data():
    try:
        # Assuming GFSI data is on a sheet named 'Overall Scores' or similar.
        # You might need to change 'Overall Scores' to the actual sheet name
        # in your 'Economist_Impact_GFSI_2022_Model_Sep_2022 (1).xlsm' file.
        # If your GFSI data is on a different sheet number, change sheet_name= to that number (e.g., sheet_name=1).
        gfsi_df = pd.read_excel(
            "Economist_Impact_GFSI_2022_Model_Sep_2022 (1).xlsm",
            sheet_name='Overall Scores' # IMPORTANT: Change this to your actual GFSI sheet name or index (e.g., 1)
        )
        gfsi_df.columns = gfsi_df.columns.str.strip()

        # IMPORTANT: Rename columns to match the dashboard's expected names for GFSI.
        # You MUST verify these 'Old Column Name': 'New Column Name' mappings
        # against the actual column headers in your Excel file for GFSI data.
        # Common GFSI column names might be 'Country', 'Economy', 'Overall Score', 'Score_2022', etc.
        gfsi_df = gfsi_df.rename(columns={
            'Country': 'Country', # Example: Replace 'Country' with your actual country column name
            'Overall Score': 'GFSI Score', # Example: Replace with your actual GFSI score column name
            # Add other relevant GFSI dimensions if you want to use them in tables/filters later
            # e.g., 'Food availability': 'Food Availability Score',
            # 'Affordability': 'Affordability Score',
            # 'Quality and Safety': 'Quality and Safety Score',
            # 'Sustainability and Adaptation': 'Sustainability Score'
        })

        required_gfsi_columns = ['Country', 'GFSI Score']
        for col in required_gfsi_columns:
            if col not in gfsi_df.columns:
                st.error(f"Error in GFSI data: Required column '{col}' not found after renaming. "
                         f"Please check your Excel file's column names and the renaming logic in app.py for GFSI data.")
                return pd.DataFrame(columns=required_gfsi_columns)

        gfsi_df['GFSI Score'] = pd.to_numeric(gfsi_df['GFSI Score'], errors='coerce')
        gfsi_df = gfsi_df.dropna(subset=required_gfsi_columns)
        return gfsi_df
    except FileNotFoundError:
        st.error("Error: Excel file 'Economist_Impact_GFSI_2022_Model_Sep_2022 (1).xlsm' not found. "
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
    st.markdown("A prototype dashboard to identify cost-effective protein-rich foods based on expert research.")

    st.sidebar.header("Protein Filters")
    st.sidebar.markdown("Adjust the sliders and selections below to find the best protein sources.")

    # Protein Region Filter
    if 'Region' in protein_data.columns and not protein_data['Region'].empty:
        protein_regions = st.sidebar.multiselect(
            "Select Region(s) (Protein)",
            options=protein_data['Region'].unique(),
            default=protein_data['Region'].unique(),
            help="Filter foods available in specific regions for protein analysis."
        )
    else:
        st.sidebar.warning("Protein Region data not available or empty. Cannot filter by region.")
        protein_regions = []

    # Protein Index Range Slider
    # Set dynamic min/max for slider based on actual data
    min_protein_index_data = int(protein_data['Protein Index'].min()) if 'Protein Index' in protein_data.columns and not protein_data['Protein Index'].empty else 0
    max_protein_index_data = int(protein_data['Protein Index'].max()) if 'Protein Index' in protein_data.columns and not protein_data['Protein Index'].empty else 100
    
    # Ensure default slider values are within the actual data range
    default_min_index = min_protein_index_data
    default_max_index = max_protein_index_data
    if min_protein_index_data <= 70 <= max_protein_index_data:
        default_min_index = 70
    if min_protein_index_data <= 100 <= max_protein_index_data:
        default_max_index = 100

    min_index, max_index = st.sidebar.slider(
        "Protein Index Range (Protein)",
        min_value=min_protein_index_data,
        max_value=max_protein_index_data,
        value=(default_min_index, default_max_index),
        step=5,
        help="Filter foods by their protein content efficiency (higher is better)."
    )

    # Max Cost per gram protein Slider
    # Set dynamic min/max for slider based on actual data
    min_cost_data = float(protein_data['Cost per gram protein'].min()) if 'Cost per gram protein' in protein_data.columns and not protein_data['Cost per gram protein'].empty else 0.1
    max_cost_data = float(protein_data['Cost per gram protein'].max()) if 'Cost per gram protein' in protein_data.columns and not protein_data['Cost per gram protein'].empty else 5.0

    # Ensure default slider value is within the actual data range
    default_max_cost = 1.0
    if min_cost_data <= 1.0 <= max_cost_data:
        default_max_cost = 1.0
    elif max_cost_data < 1.0:
        default_max_cost = max_cost_data # If max data is less than 1.0, set default to max data
    elif min_cost_data > 1.0:
        default_max_cost = min_cost_data # If min data is greater than 1.0, set default to min data

    max_cost = st.sidebar.slider(
        "Max Cost per gram protein (USD) (Protein)",
        min_value=min_cost_data,
        max_value=max_cost_data,
        value=default_max_cost,
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
        filtered_protein_data = pd.DataFrame() # If data loading failed, filtered_protein_data is empty

    st.subheader("Filtered Protein Sources Table")
    if filtered_protein_data.empty:
        st.warning("No protein sources match the selected filters or protein data could not be loaded. Please adjust your selections or check the Excel file.")
    else:
        st.dataframe(filtered_protein_data, use_container_width=True, height=250)

    st.subheader("Protein Index vs. Cost per gram protein")
    st.markdown("This chart visualizes the relationship between protein efficiency and cost. Look for items in the top-left quadrant (high protein index, low cost).")
    if not filtered_protein_data.empty:
        # Check if 'Food' column exists before plotting
        if 'Food' not in filtered_protein_data.columns:
            st.error("Error: 'Food' column not found in filtered protein data. Cannot create scatter plot.")
        else:
            fig_protein = px.scatter(
                filtered_protein_data,
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
        
        # Calculate and display averages only if filtered_protein_data is not empty
        if not filtered_protein_data['Protein Index'].empty:
            st.markdown(f"**Average Protein Index** of filtered foods: **{filtered_protein_data['Protein Index'].mean():.2f}**")
        else:
            st.markdown("Average Protein Index: N/A (no data)")

        if not filtered_protein_data['Cost per gram protein'].empty:
            st.markdown(f"**Average Cost per gram protein** of filtered foods: **${filtered_protein_data['Cost per gram protein'].mean():.2f}**")
        else:
            st.markdown("Average Cost per gram protein: N/A (no data)")

        # Identify the most cost-effective food in the filtered list
        if not filtered_protein_data.empty and 'Cost per gram protein' in filtered_protein_data.columns and not filtered_protein_data['Cost per gram protein'].empty:
            most_cost_effective = filtered_protein_data.loc[filtered_protein_data['Cost per gram protein'].idxmin()]
            st.markdown(f"The most **cost-effective** protein source in the filtered list is **{most_cost_effective['Food']}** (Protein Index: {most_cost_effective['Protein Index']}, Cost: ${most_cost_effective['Cost per gram protein']:.2f}/g protein).")
        else:
            st.markdown("Most cost-effective protein source: N/A (no data)")

        # Identify the highest protein index food in the filtered list
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
            default=gfsi_data['Country'].unique(),
            help="Filter countries for GFSI analysis."
        )
    else:
        st.sidebar.warning("GFSI Country data not available or empty. Cannot filter by country.")
        gfsi_countries = []

    # GFSI Score Range Slider
    # Set dynamic min/max for slider based on actual data
    min_gfsi_score_data = int(gfsi_data['GFSI Score'].min()) if 'GFSI Score' in gfsi_data.columns and not gfsi_data['GFSI Score'].empty else 0
    max_gfsi_score_data = int(gfsi_data['GFSI Score'].max()) if 'GFSI Score' in gfsi_data.columns and not gfsi_data['GFSI Score'].empty else 100

    min_gfsi_score, max_gfsi_score = st.sidebar.slider(
        "GFSI Score Range (GFSI)",
        min_value=min_gfsi_score_data,
        max_value=max_gfsi_score_data,
        value=(min_gfsi_score_data, max_gfsi_score_data), # Default to full range of loaded data
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
        filtered_gfsi_data = pd.DataFrame() # If data loading failed, filtered_gfsi_data is empty

    st.subheader("Filtered GFSI Data Table")
    if filtered_gfsi_data.empty:
        st.warning("No GFSI data matches the selected filters or GFSI data could not be loaded. Please adjust your selections or check the Excel file.")
    else:
        st.dataframe(filtered_gfsi_data, use_container_width=True, height=300)

    st.subheader("Global Food Security Index Map")
    st.markdown("This map visualizes GFSI scores by country. Higher scores indicate better food security.")

    if not filtered_gfsi_data.empty:
        # Ensure 'Country' and 'GFSI Score' columns are present for mapping
        if 'Country' not in filtered_gfsi_data.columns or 'GFSI Score' not in filtered_gfsi_data.columns:
            st.error("Error: 'Country' or 'GFSI Score' column not found in filtered GFSI data. Cannot create map.")
        else:
            fig_gfsi = px.choropleth(
                filtered_gfsi_data,
                locations="Country",
                locationmode="country names", # Crucial for mapping country names to geographical data
                color="GFSI Score",
                hover_name="Country",
                color_continuous_scale=px.colors.sequential.Plasma, # A good color scale for scores
                title="Global Food Security Index by Country",
                labels={'GFSI Score': 'GFSI Score'},
                height=600 # Adjust map height as needed
            )
            fig_gfsi.update_layout(
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    projection_type='equirectangular' # Or 'natural earth', 'orthographic' etc.
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

        # Ensure these operations are safe even if filtered_gfsi_data is very small or has all same values
        if not filtered_gfsi_data['GFSI Score'].empty and filtered_gfsi_data['GFSI Score'].nunique() > 0:
            highest_score_country = filtered_gfsi_data.loc[filtered_gfsi_data['GFSI Score'].idxmax()]
            st.markdown(f"Country with the **highest GFSI Score**: **{highest_score_country['Country']}** ({highest_score_country['GFSI Score']:.2f})")

            lowest_score_country = filtered_gfsi_data.loc[filtered_gfsi_data['GFSI Score'].idxmin()]
            st.markdown(f"Country with the **lowest GFSI Score**: **{lowest_score_country['Country']}** ({lowest_score_country['GFSI Score']:.2f})")
        else:
            st.markdown("Cannot determine highest/lowest GFSI score (insufficient data or all scores are identical).")
