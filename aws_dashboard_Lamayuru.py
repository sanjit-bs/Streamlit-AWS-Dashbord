import streamlit as st
import pandas as pd
import plotly.express as px

# Google Sheet CSV link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyAh0U0ampsm5z8VncvXNaoyp9TxTMBOhs3GJH7S2JXdWQGXaYOtC1tENpFpbGZdUPAw8XKP5vlkgo/pub?gid=2093188993&single=true&output=csv"

st.set_page_config(page_title="LAMAYURU AWS Dashboard", layout="wide")

# Add logos
left_logo = "https://cuetsamarth.com/wp-content/uploads/2024/01/CENTRAL_UNIVERSITY_OF_JHARKHAND_logo-removebg-preview.png"
right_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Ministry_of_Science_and_Technology_India.svg/1200px-Ministry_of_Science_and_Technology_India.svg.png"

st.markdown(
    f"""
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <img src="{left_logo}" width="120">
        <img src="{right_logo}" width="120">
    </div>
    """,
    unsafe_allow_html=True
)

st.title("AUTOMATIC WEATHER STATION (LAMAYURU)")

# Load data
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(CSV_URL)
    timestamp_col = df.columns[0]
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors="coerce")
    df = df.dropna(subset=[timestamp_col])
    df["Date"] = df[timestamp_col].dt.date
    df["Time"] = df[timestamp_col].dt.time
    return df, timestamp_col

df, timestamp_col = load_data()
df["Date"] = pd.to_datetime(df["Date"]).dt.date

# Create a full daily time range (00:00–23:30, 30-min step)
full_time_index = pd.date_range("00:00", "23:30", freq="30min").time

# Date range selector
min_date, max_date = df["Date"].min(), df["Date"].max()
date_range = st.date_input(
    "📅 Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Handle single date vs range
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = [pd.to_datetime(d).date() for d in date_range]
    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
else:
    chosen_date = pd.to_datetime(date_range).date()
    filtered_df = df[df["Date"] == chosen_date]

# Expand data so x-axis always 00:00 → 23:30
expanded = []
for date in filtered_df["Date"].unique():
    day_df = filtered_df[filtered_df["Date"] == date].copy()
    time_df = pd.DataFrame({"Time": full_time_index})
    day_df = pd.merge(time_df, day_df, on="Time", how="left")
    day_df["Date"] = date
    expanded.append(day_df)

if expanded:
    plot_df = pd.concat(expanded)
else:
    plot_df = pd.DataFrame()

# Plot precipitation
if not plot_df.empty:
    fig = px.line(
        plot_df,
        x="Time",
        y="2.Percipitation (mm)",
        color="Date",
        title="Precipitation Over Time (by Date)",
        markers=True
    )
    fig.update_xaxes(dtick=4)  # Show fewer ticks
    st.plotly_chart(fig, use_container_width=True)

    # Wind rose plot with fixed 8 cardinal directions
    # Convert wind direction to numeric
    filtered_df["6. Wind Direction (degree)"] = pd.to_numeric(
        filtered_df["6. Wind Direction (degree)"], errors="coerce"
    )
    wind_df = filtered_df.dropna(subset=["6. Wind Direction (degree)"])

    if not wind_df.empty:
        # Define 8 fixed cardinal directions
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

        # Convert degrees to 8 cardinal directions
        def deg_to_cardinal_8(deg):
            ix = int((deg + 22.5) / 45) % 8
            return directions[ix]

        wind_df["Wind_Direction"] = wind_df["6. Wind Direction (degree)"].apply(deg_to_cardinal_8)

        # Count occurrences per direction and ensure all directions are present
        wind_counts = wind_df.groupby("Wind_Direction").size().reindex(directions, fill_value=0).reset_index(name="Count")

        # Plot wind rose
        fig_wind = px.bar_polar(
            wind_counts,
            r="Count",
            theta="Wind_Direction",
            color="Count",
            color_continuous_scale=px.colors.sequential.Rainbow,
            title="Wind Directions",
            width=700,   # set desired width
            height=700   # set desired height
        )

        # Adjust title position and spacing
        fig_wind.update_layout(
        title=dict(
        text="Wind Direction",
        y=0.95,        # vertical position (1.0 is top)
        x=0.5,         # horizontal center
        xanchor='center',
        yanchor='top',
        pad=dict(t=5)  # reduce top padding
          )
        )
        st.plotly_chart(fig_wind, use_container_width=True, config = {
    "displaylogo": False,
    "displayModeBar": True,
    "scrollZoom": True,
    "modeBarButtonsToAdd": [
        "autoScale2d", "resetScale2d",
        "zoomIn2d", "zoomOut2d", "zoom2d",
        "pan2d", "select2d", "lasso2d",
        "toImage"
        ]
      })
    else:
        st.warning("⚠️ No wind data available for the selected date range.")

    st.subheader("📊 Filtered Data")
    st.dataframe(filtered_df)
else:

    st.warning("⚠️ No data available for the selected date range.")


















