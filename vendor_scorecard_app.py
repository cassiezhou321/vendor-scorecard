import pandas as pd
import streamlit as st
import plotly.express as px

# Load data from CSV
df = pd.read_csv("streamlit_vendor_scorecard.csv")

st.title("📊 Vendor Scorecard Dashboard")

# Sidebar filters
vendors = df["Vendor"].unique()
selected_vendor = st.sidebar.selectbox("Select Vendor", vendors)

quarters = df[df["Vendor"] == selected_vendor]["Quarter"].unique()
selected_quarter = st.sidebar.selectbox("Select Quarter", quarters)

# Filter data
filtered_df = df[
    (df["Vendor"] == selected_vendor) &
    (df["Quarter"] == selected_quarter) &
    (df["Category"] != "Total")
]

st.header(f"Vendor: {selected_vendor} — {selected_quarter}")

# Bar chart
fig = px.bar(
    filtered_df,
    x="Category",
    y="Score",
    color="Category",
    title="Average Score by Category",
    labels={"Score": "Average Score"}
)
st.plotly_chart(fig)

# Radar chart
st.subheader("Subcategory Breakdown")
subcategory_fig = px.line_polar(
    filtered_df,
    r="Score",
    theta="Subcategory",
    line_close=True,
    color="Category",
    title="Subcategory Radar Chart"
)
st.plotly_chart(subcategory_fig)

# Total score
total_score = df[
    (df["Vendor"] == selected_vendor) &
    (df["Quarter"] == selected_quarter) &
    (df["Category"] == "Total")
]["Score"].values[0]

st.metric(label="Total Weighted Score", value=round(total_score, 2))
