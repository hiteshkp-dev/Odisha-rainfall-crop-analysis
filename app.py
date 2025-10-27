# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# ===============================================
# 1️⃣ PAGE CONFIG
# ===============================================
st.set_page_config(page_title="Odisha Rainfall & Crop Dashboard", layout="wide")

st.title("🌾 Odisha Rainfall & Crop Analysis Dashboard")

st.markdown("""
### 📘 Project Overview
This Streamlit dashboard analyzes Odisha’s rainfall and crop production data 
from 2010–2024. It helps identify rainfall trends, seasonal changes, 
and correlations with agricultural yields across districts.  

**Developed for the Bharat Digital Fellowship**, it showcases how open 
data and visualization can support data-driven decision-making.
""")

st.markdown("---")

# ===============================================
# 2️⃣ LOAD DATA
# ===============================================

@st.cache_data
def load_data():
    try:
        crop_rainfall_df = pd.read_csv("combined_odisha_crop_rainfall.csv")
        common_df = pd.read_csv("common_districts.csv")
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

    # Normalize column names
    crop_rainfall_df.columns = [c.strip().lower() for c in crop_rainfall_df.columns]
    common_df.columns = [c.strip().lower() for c in common_df.columns]

    # Handle variations in district column name
    for col in crop_rainfall_df.columns:
        if "district" in col:
            crop_rainfall_df.rename(columns={col: "district"}, inplace=True)
    for col in common_df.columns:
        if "district" in col:
            common_df.rename(columns={col: "district"}, inplace=True)

    return crop_rainfall_df, common_df

crop_rainfall_df, common_df = load_data()

if crop_rainfall_df is None or common_df is None:
    st.stop()

# ===============================================
# 3️⃣ FILTER SIDEBAR
# ===============================================

st.sidebar.header("🔍 Filters")

districts = sorted(common_df["district"].unique())
selected_district = st.sidebar.selectbox("Select District", districts)

years = sorted(crop_rainfall_df["year"].dropna().unique())
selected_year = st.sidebar.selectbox("Select Year", years)

months = sorted(crop_rainfall_df["month"].dropna().unique())
selected_month = st.sidebar.selectbox("Select Month", months)

# ===============================================
# 4️⃣ FILTER DATA
# ===============================================

filtered_df = crop_rainfall_df[
    (crop_rainfall_df["district"] == selected_district)
    & (crop_rainfall_df["year"] == selected_year)
]

# ===============================================
# 5️⃣ METRICS & INSIGHTS
# ===============================================

if not filtered_df.empty:
    st.subheader(f"📊 Insights for {selected_district} - {selected_year}")

    col1, col2, col3 = st.columns(3)
    col1.metric("🌧️ Avg Rainfall (mm)", f"{filtered_df['avg_rainfall'].mean():.2f}")
    col2.metric("🌿 Main Crop", filtered_df["crop"].mode()[0])
    col3.metric("📅 Seasons", filtered_df["season"].nunique())

    st.markdown("---")

    st.subheader("🌦️ Monthly Rainfall Trend")

    fig = px.line(
        filtered_df,
        x="month",
        y="avg_rainfall",
        color="season",
        markers=True,
        title=f"Rainfall Trend for {selected_district} ({selected_year})",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("🌾 Crop vs Rainfall Data")
    st.dataframe(filtered_df[["crop", "season", "area", "production", "avg_rainfall"]])

    st.markdown("---")
    st.subheader("🔍 Auto Insights")
    st.write(f"""
    - 🌦️ **Peak Rainfall Month:** {filtered_df.loc[filtered_df['avg_rainfall'].idxmax(), 'month']}
    - 📊 **Average Rainfall:** {filtered_df['avg_rainfall'].mean():.2f} mm
    - 🌾 **Most Grown Crop:** {filtered_df['crop'].mode()[0]}
    - 📈 **Average Production:** {filtered_df['production'].mean():.2f}
    """)
else:
    st.warning("⚠️ No data available for the selected filters.")

st.markdown("---")
st.caption("🧠 Created by Hitesh Kumar Padhiary | Bharat Digital Fellowship 2026")


