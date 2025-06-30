# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load Data from Excel File ---
# Use st.cache_data to cache the data loading,
# so it only runs once when the app starts or the file changes.
@st.cache_data
def load_data():
    try:
        # Read the Excel file.
        # Ensure 'Economist_Impact_GFSI_2022_Model_Sep_2022 (1).xlsm' is in the same directory
        # as this app.py file, or provide the full path to the file.
        # sheet_name=0 reads the first sheet. Change this if your data is on a different sheet
        # (e.g., sheet_name="YourSheetName").
        df = pd.read_excel(
            "Economist_Impact_GFSI_2022_Model_Sep_2022 (1).xlsm",
            sheet_name=0
        )
        
        # Strip whitespace from column names to ensure clean matching
        df.columns = df.columns.str.strip()

        # IMPORTANT: Rename columns to match the dashboard's expected names.
        # You MUST verify these 'Old Column Name': 'New Column Name' mappings
        # against the actual column headers in your Excel file.
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
                st.error(f"Error: Required column '{col}' not found after renaming. "
                         f"Please check your Excel file's column names and the renaming logic in app.py.")
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
        st.error(f"An error occurred while loading data: {e}")
        return pd.DataFrame() # Return an empty DataFrame on other errors

# Load the data when the app starts
data = load_data()

# --- Streamlit Page Configuration ---
st.set_page_config(layout="wide", page_title="Protein Index Dashboard")

# --- Dashboard Title ---
st.title("Protein Index & Affordability Dashboard")
st.markdown("A prototype dashboard to identify cost-effective protein-rich foods based on expert research.")

# --- Sidebar for Filters ---
st.sidebar.header("Filter Options")
st.sidebar.markdown("Adjust the sliders and selections below to find the best protein sources.")

# Check if 'Region' column exists and has unique values before creating multiselect
if 'Region' in data.columns and not data['Region'].empty:
    regions = st.sidebar.multiselect(
        "Select Region(s)",
        options=data['Region'].unique(),
        default=data['Region'].unique(), # Default to all regions selected
        help="Filter foods available in specific regions."
    )
else:
    st.sidebar.warning("Region data not available or empty. Cannot filter by region.")
    regions = [] # Set regions to empty list if data is missing

# Ensure min_value and max_value for slider are appropriate for 'Protein Index'
min_protein_index_data = int(data['Protein Index'].min()) if 'Protein Index' in data.columns and not data['Protein Index'].empty else 0
max_protein_index_data = int(data['Protein Index'].max()) if 'Protein Index' in data.columns and not data['Protein Index'].empty else 100

min_index, max_index = st.sidebar.slider(
    "Protein Index Range",
    min_value=min_protein_index_data,
    max_value=max_protein_index_data,
    value=(min(70, max_protein_index_data), max(100, min_protein_index_data)), # Default to a sensible range
    step=5,
    help="Filter foods by their protein content efficiency (higher is better)."
)

# Ensure min_value and max_value for slider are appropriate for 'Cost per gram protein'
min_cost_data = float(data['Cost per gram protein'].min()) if 'Cost per gram protein' in data.columns and not data['Cost per gram protein'].empty else 0.1
max_cost_data = float(data['Cost per gram protein'].max()) if 'Cost per gram protein' in data.columns and not data['Cost per gram protein'].empty else 5.0

max_cost = st.sidebar.slider(
    "Max Cost per gram protein (USD)",
    min_value=min_cost_data,
    max_value=max_cost_data,
    value=min(1.0, max_cost_data), # Default to a sensible max cost
    step=0.05,
    help="Filter foods based on their affordability (lower cost is better)."
)

# --- Apply Filters to Data ---
# Check if data is loaded before applying filters
if not data.empty:
    filtered_data = data[
        (data['Region'].isin(regions)) &
        (data['Protein Index'].between(min_index, max_index)) &
        (data['Cost per gram protein'] <= max_cost)
    ]
else:
    filtered_data = pd.DataFrame() # If data loading failed, filtered_data is empty

# --- Display Filtered Data ---
st.subheader("Filtered Protein Sources Table")
if filtered_data.empty:
    st.warning("No protein sources match the selected filters or data could not be loaded. Please adjust your selections or check the Excel file.")
else:
    # Display the filtered data in an interactive table.
    st.dataframe(filtered_data, use_container_width=True, height=250) # Set a fixed height for consistency

# --- Create and Display Scatter Plot ---
st.subheader("Protein Index vs. Cost per gram protein")
st.markdown("This chart visualizes the relationship between protein efficiency and cost. Look for items in the top-left quadrant (high protein index, low cost).")

if filtered_data.empty:
    st.info("No data to display in the chart. Adjust filters to see results.")
else:
    # Check if 'Food' column exists before plotting
    if 'Food' not in filtered_data.columns:
        st.error("Error: 'Food' column not found in filtered data. Cannot create scatter plot.")
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
    
    # Calculate and display averages only if filtered_data is not empty
    if not filtered_data['Protein Index'].empty:
        st.markdown(f"**Average Protein Index** of filtered foods: **{filtered_data['Protein Index'].mean():.2f}**")
    else:
        st.markdown("Average Protein Index: N/A (no data)")

    if not filtered_data['Cost per gram protein'].empty:
        st.markdown(f"**Average Cost per gram protein** of filtered foods: **${filtered_data['Cost per gram protein'].mean():.2f}**")
    else:
        st.markdown("Average Cost per gram protein: N/A (no data)")

    # Identify the most cost-effective food in the filtered list
    if not filtered_data.empty and 'Cost per gram protein' in filtered_data.columns:
        most_cost_effective = filtered_data.loc[filtered_data['Cost per gram protein'].idxmin()]
        st.markdown(f"The most **cost-effective** protein source in the filtered list is **{most_cost_effective['Food']}** (Protein Index: {most_cost_effective['Protein Index']}, Cost: ${most_cost_effective['Cost per gram protein']:.2f}/g protein).")
    else:
        st.markdown("Most cost-effective protein source: N/A (no data)")

    # Identify the highest protein index food in the filtered list
    if not filtered_data.empty and 'Protein Index' in filtered_data.columns:
        highest_protein_index = filtered_data.loc[filtered_data['Protein Index'].idxmax()]
        st.markdown(f"The protein source with the **highest Protein Index** is **{highest_protein_index['Food']}** (Protein Index: {highest_protein_index['Protein Index']}, Cost: ${highest_protein_index['Cost per gram protein']:.2f}/g protein).")
    else:
        st.markdown("Highest protein index food: N/A (no data)")
