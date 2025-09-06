import streamlit as st
import pandas as pd
import plotly.express as px

# Google Sheet CSV link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyAh0U0ampsm5z8VncvXNaoyp9TxTMBOhs3GJH7S2JXdWQGXaYOtC1tENpFpbGZdUPAw8XKP5vlkgo/pub?gid=2093188993&single=true&output=csv"

st.set_page_config(page_title="LAMAYURU AWS Dashboard", layout="wide")

)
st.title("🌦️ LAMAYURU AWS Dashboard")

# Load data
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(CSV_URL)
    # Detect timestamp column
    timestamp_col = df.columns[0]
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors="coerce")
    df = df.dropna(subset=[timestamp_col])
    df["Date"] = df[timestamp_col].dt.date
    df["Time"] = df[timestamp_col].dt.time
    return df, timestamp_col

df, timestamp_col = load_data()
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# Date range selector
min_date, max_date = df["Date"].min(), df["Date"].max()
date_range = st.date_input(
    "📅 Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Handle both single-date and range inputs
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = [pd.to_datetime(d).date() for d in date_range]
    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
else:
    chosen_date = pd.to_datetime(date_range).date()
    filtered_df = df[df["Date"] == chosen_date]

# Plot precipitation
if not filtered_df.empty:
    fig = px.line(
        filtered_df,
        x="Time",
        y="2.Percipitation (mm)",
        color="Date",
        title="Precipitation Over Time (by Date)",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Filtered Data")
    st.dataframe(filtered_df)
else:

    st.warning("⚠️ No data available for the selected date range.")


