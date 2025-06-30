# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load Data from Excel File ---
@st.cache_data
def load_data():
    df = pd.read_excel(
        "Economist_Impact_GFSI_2022_Model_Sep_2022 (1).xlsm",
        sheet_name=0  # You can also specify the exact sheet name if known
    )
    # Rename or select the required columns based on actual content
    df = df.rename(columns=lambda x: x.strip())  # Strip whitespace

    # Dummy mapping for example, replace with actual column names
    df = df.rename(columns={
        'Food Name': 'Food',
        'Protein Efficiency Index': 'Protein Index',
        'Cost USD/g protein': 'Cost per gram protein',
        'Geographic Region': 'Region'
    })

    # Drop rows with missing required fields
    df = df.dropna(subset=['Food', 'Protein Index', 'Cost per gram protein', 'Region'])
    return df

# Load real data
data = load_data()

# --- Streamlit Page Configuration ---
st.set_page_config(layout="wide", page_title="Protein Index Dashboard")

# --- Dashboard Title ---
st.title("Protein Index & Affordability Dashboard")
st.markdown("A prototype dashboard to identify cost-effective protein-rich foods based on expert research.")

# --- Sidebar for Filters ---
st.sidebar.header("Filter Options")
st.sidebar.markdown("Adjust the sliders and selections below to find the best protein sources.")

regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=data['Region'].unique(),
    default=data['Region'].unique(),
    help="Filter foods available in specific regions."
)

min_index, max_index = st.sidebar.slider(
    "Protein Index Range",
    min_value=0,
    max_value=100,
    value=(70, 100),
    step=5,
    help="Filter foods by their protein content efficiency (higher is better)."
)

max_cost = st.sidebar.slider(
    "Max Cost per gram protein (USD)",
    min_value=0.1,
    max_value=5.0,
    value=1.0,
    step=0.05,
    help="Filter foods based on their affordability (lower cost is better)."
)

# --- Apply Filters ---
filtered_data = data[
    (data['Region'].isin(regions)) &
    (data['Protein Index'].between(min_index, max_index)) &
    (data['Cost per gram protein'] <= max_cost)
]

# --- Display Table ---
st.subheader("Filtered Protein Sources Table")
if filtered_data.empty:
    st.warning("No protein sources match the selected filters. Please adjust your selections.")
else:
    st.dataframe(filtered_data, use_container_width=True, height=250)

# --- Scatter Plot ---
st.subheader("Protein Index vs. Cost per gram protein")
st.markdown("This chart visualizes the relationship between protein efficiency and cost. Look for items in the top-left quadrant (high protein index, low cost).")
if not filtered_data.empty:
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

# --- Insights ---
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
