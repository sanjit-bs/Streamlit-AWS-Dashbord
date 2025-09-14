# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # Google Sheet CSV link
# CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyAh0U0ampsm5z8VncvXNaoyp9TxTMBOhs3GJH7S2JXdWQGXaYOtC1tENpFpbGZdUPAw8XKP5vlkgo/pub?gid=2093188993&single=true&output=csv"

# st.set_page_config(page_title="LAMAYURU AWS Dashboard", layout="wide")

# # Add logos
# left_logo = "https://cuetsamarth.com/wp-content/uploads/2024/01/CENTRAL_UNIVERSITY_OF_JHARKHAND_logo-removebg-preview.png"
# right_logo = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Ministry_of_Science_and_Technology_India.svg/1200px-Ministry_of_Science_and_Technology_India.svg.png"

# st.markdown(
#     f"""
#     <div style='display: flex; justify-content: space-between; align-items: center;'>
#         <img src="{left_logo}" width="120">
#         <img src="{right_logo}" width="120">
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# st.title("AUTOMATIC WEATHER STATION (LAMAYURU)")

# # Load data
# @st.cache_data(ttl=60)
# def load_data():
#     df = pd.read_csv(CSV_URL)
#     timestamp_col = df.columns[0]
#     df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors="coerce")
#     df = df.dropna(subset=[timestamp_col])
#     df["Date"] = df[timestamp_col].dt.date
#     df["Time"] = df[timestamp_col].dt.time
#     return df, timestamp_col

# df, timestamp_col = load_data()
# df["Date"] = pd.to_datetime(df["Date"]).dt.date

# # Create a full daily time range (00:00–23:30, 30-min step)
# full_time_index = pd.date_range("00:00", "23:30", freq="30min").time

# # Date range selector
# min_date, max_date = df["Date"].min(), df["Date"].max()
# date_range = st.date_input(
#     "📅 Select Date Range",
#     [min_date, max_date],
#     min_value=min_date,
#     max_value=max_date
# )

# # Handle single date vs range
# if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
#     start_date, end_date = [pd.to_datetime(d).date() for d in date_range]
#     filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
# else:
#     chosen_date = pd.to_datetime(date_range).date()
#     filtered_df = df[df["Date"] == chosen_date]

# # Expand data so x-axis always 00:00 → 23:30
# expanded = []
# for date in filtered_df["Date"].unique():
#     day_df = filtered_df[filtered_df["Date"] == date].copy()
#     time_df = pd.DataFrame({"Time": full_time_index})
#     day_df = pd.merge(time_df, day_df, on="Time", how="left")
#     day_df["Date"] = date
#     expanded.append(day_df)

# if expanded:
#     plot_df = pd.concat(expanded)
# else:
#     plot_df = pd.DataFrame()

# # Plot precipitation
# if not plot_df.empty:
#     fig = px.line(
#         plot_df,
#         x="Time",
#         y="2.Percipitation (mm)",
#         color="Date",
#         title="Precipitation Over Time (by Date)",
#         markers=True
#     )
#     fig.update_xaxes(dtick=4)  # Show fewer ticks
#     st.plotly_chart(fig, use_container_width=True)

#     # Wind rose plot with fixed 8 cardinal directions
#     # Convert wind direction to numeric
#     filtered_df["6. Wind Direction (degree)"] = pd.to_numeric(
#         filtered_df["6. Wind Direction (degree)"], errors="coerce"
#     )
#     wind_df = filtered_df.dropna(subset=["6. Wind Direction (degree)"])

#     if not wind_df.empty:
#         # Define 8 fixed cardinal directions
#         directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

#         # Convert degrees to 8 cardinal directions
#         def deg_to_cardinal_8(deg):
#             ix = int((deg + 22.5) / 45) % 8
#             return directions[ix]

#         wind_df["Wind_Direction"] = wind_df["6. Wind Direction (degree)"].apply(deg_to_cardinal_8)

#         # Count occurrences per direction and ensure all directions are present
#         wind_counts = wind_df.groupby("Wind_Direction").size().reindex(directions, fill_value=0).reset_index(name="Count")

#         # Plot wind rose
#         fig_wind = px.bar_polar(
#             wind_counts,
#             r="Count",
#             theta="Wind_Direction",
#             color="Count",
#             color_continuous_scale=px.colors.sequential.Rainbow,
#             title="Wind Directions",
#             width=700,   # set desired width
#             height=700   # set desired height
#         )

#         # Adjust title position and spacing
#         fig_wind.update_layout(
#         title=dict(
#         text="Wind Direction",
#         y=0.95,        # vertical position (1.0 is top)
#         x=0.5,         # horizontal center
#         xanchor='center',
#         yanchor='top',
#         pad=dict(t=5)  # reduce top padding
#           )
#         )
        
#         # Config for interactive buttons
#         config = {
#         "displaylogo": False,
#         "displayModeBar": True,
#         "scrollZoom": True,
#         "modeBarButtonsToAdd": [
#             "autoScale2d", "resetScale2d",
#             "zoomIn2d", "zoomOut2d", "zoom2d",
#             "pan2d", "toImage"
#           ]
#         }
    
#         st.plotly_chart(fig_wind, use_container_width=True, config=config)
#     else:
#         st.warning("⚠️ No wind data available for the selected date range.")

#     st.subheader("📈 Filtered Data")
#     st.dataframe(filtered_df)
# else:

#     st.warning("⚠️ No data available for the selected date range.")

###########################################################################################################################################################
###########################################################################################################################################################

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt

# Google Sheet CSV link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQyAh0U0ampsm5z8VncvXNaoyp9TxTMBOhs3GJH7S2JXdWQGXaYOtC1tENpFpbGZdUPAw8XKP5vlkgo/pub?gid=2093188993&single=true&output=csv"

st.set_page_config(page_title="LAMAYURU AWS Dashboard", layout="wide")

# ---------------- Sticky Header ----------------
st.markdown("""
    <div class="fixed-header">
        <div class="header-container">
            <img class="logo1" src="https://cuetsamarth.com/wp-content/uploads/2024/01/CENTRAL_UNIVERSITY_OF_JHARKHAND_logo-removebg-preview.png" alt="CUJ Logo">
            <div class="header-text">
            <div class="header-title">AUTOMATIC WEATHER STATION (LAMAYURU, LADAKH)</div>
            <div class="header-subtitle">Department of Geoinformatics</div>
            </div>
            <img class="logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Ministry_of_Science_and_Technology_India.svg/1200px-Ministry_of_Science_and_Technology_India.svg.png" alt="MST Logo">
        </div>
    </div>

    <style>
    .fixed-header {
        position: fixed;
        top: 3.5rem;  /* 👈 Push below Streamlit’s default top bar */
        left: 0;
        width: 100%;
        z-index: 1000;
        background: #87CEEB;  /* 🌤️ Sky blue panel */
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        padding: 5px 0;
    }
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        max-width: 1200px;
        margin: auto;
        padding: 0 20px;
    }
    .header-text {
        text-align: center;
        flex: 1;
    }
    .header-title {
        font-size: 24px;
        font-weight: bold;
        color: #02590F; /* DarkGreen */
    }
    .header-subtitle {
        font-size: 20px;
        font-weight: bold;
        color: #333;
        margin-top: 2px;
    }
    .logo {
        height: 100px;
        width: auto;
        object-fit: contain;
    }
    .logo1 {
        height: 150px;
        width: auto;
        object-fit: contain;
    }
    </style>
""", unsafe_allow_html=True)

# Add space below header so content doesn’t overlap
st.markdown("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

# ---------------- Data Loading ----------------
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

# ---------------- Precipitation Plot ----------------
if not plot_df.empty:
    fig = px.line(plot_df, x="Time", y="2.Percipitation (mm)", color="Date",
                  title="Precipitation Over Time (by Date)", markers=True, labels={"2.Percipitation (mm)": "Precipitation (mm)"})
    fig.update_xaxes(dtick=4)
    st.plotly_chart(fig, use_container_width=True)

    # 👉 Total precipitation panel
    precip_col = "2.Percipitation (mm)"
    filtered_df[precip_col] = pd.to_numeric(filtered_df[precip_col], errors="coerce")
    total_precip = filtered_df[precip_col].sum(skipna=True)

    st.markdown(
        f"""
        <div style="background-color:#e6f2ff; padding:10px; border-radius:8px; border:1px solid #b3d1ff;
                    width:fit-content; margin-top:-5px;">
        <b>Total Precipitation:</b> {total_precip:.2f} mm
        </div>
        """, unsafe_allow_html=True
    )

    # ---------------- Wind Roses ----------------
    filtered_df["6. Wind Direction (degree)"] = pd.to_numeric(filtered_df["6. Wind Direction (degree)"], errors="coerce")
    filtered_df["5. Wind Speed (m/s)"] = pd.to_numeric(filtered_df["5. Wind Speed (m/s)"], errors="coerce")
    filtered_df["18. Gust Wind Speed (m/s)"] = pd.to_numeric(filtered_df["18. Gust Wind Speed (m/s)"], errors="coerce")

    wind_df = filtered_df.dropna(subset=["6. Wind Direction (degree)"])
    gust_df = filtered_df.dropna(subset=["6. Wind Direction (degree)", "18. Gust Wind Speed (m/s)"])

    if not wind_df.empty:
        directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

        def deg_to_cardinal_8(deg):
            ix = int((deg + 22.5) / 45) % 8
            return directions[ix]
        
        if "6. Wind Direction (degree)" in filtered_df.columns:
            filtered_df["Wind_Direction"] = pd.to_numeric(
                filtered_df["6. Wind Direction (degree)"], errors="coerce"
         ).dropna().apply(deg_to_cardinal_8)

        wind_df["Wind_Direction"] = wind_df["6. Wind Direction (degree)"].apply(deg_to_cardinal_8)
        gust_df["Wind_Direction"] = gust_df["6. Wind Direction (degree)"].apply(deg_to_cardinal_8)

        # Wind Rose (frequency)
        wind_counts = wind_df.groupby("Wind_Direction").size().reindex(directions, fill_value=0).reset_index(name="Count")
        fig_wind = px.bar_polar(wind_counts, r="Count", theta="Wind_Direction", color="Count",
                                color_continuous_scale=px.colors.sequential.Plasma, width=600, height=600)
        fig_wind.update_layout(title=dict(text="Wind Flow Directions (Count)", y=0.95, x=0.5))

        # Gust Rose (speed)
        gust_counts = gust_df.groupby("Wind_Direction")["18. Gust Wind Speed (m/s)"].mean().reindex(directions, fill_value=0).reset_index(name="Avg Gust Speed")
        fig_gust = px.bar_polar(gust_counts, r="Avg Gust Speed", theta="Wind_Direction",
                                color="Avg Gust Speed", color_continuous_scale=px.colors.sequential.Viridis,
                                width=600, height=600, title="Gust Wind Flow (Speed & Direction)")
        fig_gust.update_layout(coloraxis_colorbar=dict(title="Speed (m/s)"))

        col1, col2, col3 = st.columns([6, 3, 7])
        with col1: st.plotly_chart(fig_wind, use_container_width=True)
        with col2: st.image("Location.jpg", caption="AWS Location", width=230)
        with col3: st.plotly_chart(fig_gust, use_container_width=True)

        # # ---------------- 8 Directional Line Graphs ----------------
        # row_col_map = {"N": (1,1), "NE": (1,2), "E": (2,1), "SE": (2,2),
        #                "S": (3,1), "SW": (3,2), "W": (4,1), "NW": (4,2)}

        # fig_dir = make_subplots(rows=4, cols=2, subplot_titles=list(row_col_map.keys()))

        # for direction, (r,c) in row_col_map.items():
        #     dir_df = filtered_df[filtered_df["Wind_Direction"] == direction]
        #     if not dir_df.empty:
        #         for date in dir_df["Date"].unique():
        #             sub_df = dir_df[dir_df["Date"] == date]

        #             fig_dir.add_trace(
        #                 go.Scatter(x=sub_df["Time"], y=sub_df["5. Wind Speed (m/s)"],
        #                            mode="lines+markers", name=f"{date} - Wind",
        #                            marker=dict(size=6, color="blue"),
        #                            legendgroup="wind", showlegend=False),
        #                 row=r, col=c
        #             )
        #             fig_dir.add_trace(
        #                 go.Scatter(x=sub_df["Time"], y=sub_df["18. Gust Wind Speed (m/s)"],
        #                            mode="lines+markers", name=f"{date} - Gust",
        #                            marker=dict(size=6, color="red"),
        #                            legendgroup="gust", showlegend=False),
        #                 row=r, col=c
        #             )

        # fig_dir.update_layout(height=1200, width=1400,
        #                       title_text="Wind Speed vs Gust by Direction",
        #                       showlegend=True,
        #                       legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5))
        # st.plotly_chart(fig_dir, use_container_width=True)

    

            # ---------------- 8 Directional Line Graphs ----------------
        row_col_map = {
            "N": (1,1), "NE": (1,2),
            "E": (2,1), "SE": (2,2),
            "S": (3,1), "SW": (3,2),
            "W": (4,1), "NW": (4,2)
        }

        fig_dir = make_subplots(rows=4, cols=2, subplot_titles=list(row_col_map.keys()))

        for direction, (r, c) in row_col_map.items():
            dir_df = filtered_df[filtered_df["Wind_Direction"] == direction]

            if not dir_df.empty:
                for date in dir_df["Date"].unique():
                    sub_df = dir_df[dir_df["Date"] == date].copy()

                    # 👉 Ensure continuous time like precipitation plot
                    time_df = pd.DataFrame({"Time": full_time_index})
                    sub_df = pd.merge(time_df, sub_df, on="Time", how="left")
                    sub_df["Date"] = date

                    # Wind Speed line
                    fig_dir.add_trace(
                        go.Scatter(
                            x=sub_df["Time"], y=sub_df["5. Wind Speed (m/s)"],
                            mode="lines+markers",
                            name=f"{date} - Wind",
                            line=dict(color="blue"),
                            marker=dict(size=5),
                            legendgroup="wind",
                            showlegend=False
                        ),
                        row=r, col=c
                    )

                    # Gust Wind Speed line
                    fig_dir.add_trace(
                        go.Scatter(
                            x=sub_df["Time"], y=sub_df["18. Gust Wind Speed (m/s)"],
                            mode="lines+markers",
                            name=f"{date} - Gust",
                            line=dict(color="red"),
                            marker=dict(size=5),
                            legendgroup="gust",
                            showlegend=False
                        ),
                        row=r, col=c
                    )

                    # Highlight Peaks (Wind Speed)
                    peaks_wind = sub_df[sub_df["5. Wind Speed (m/s)"] == sub_df["5. Wind Speed (m/s)"].max()]
                    fig_dir.add_trace(
                        go.Scatter(
                            x=peaks_wind["Time"], y=peaks_wind["5. Wind Speed (m/s)"],
                            mode="markers+text",
                            #text=["Peak"],
                            textposition="top center",
                            marker=dict(color="green", size=10, symbol="star"),
                            name=f"{date} Wind Peak",
                            showlegend=False
                        ),
                        row=r, col=c
                    )

                    # Highlight Peaks (Gust Speed)
                    peaks_gust = sub_df[sub_df["18. Gust Wind Speed (m/s)"] == sub_df["18. Gust Wind Speed (m/s)"].max()]
                    fig_dir.add_trace(
                        go.Scatter(
                            x=peaks_gust["Time"], y=peaks_gust["18. Gust Wind Speed (m/s)"],
                            mode="markers+text",
                            # text=["Peak"],
                            textposition="top center",
                            marker=dict(color="green", size=10, symbol="star"),
                            name=f"{date} Gust Peak",
                            showlegend=False
                        ),
                        row=r, col=c
                    )

        fig_dir.update_layout(
            height=1400, width=1600,
            title_text="Wind Speed and Gust Wind Speed according to Directions",
            legend=dict(
                orientation="h",
                yanchor="bottom", y=-0.2,
                xanchor="center", x=0.5
            )
        )

        # Add general legend entries manually
        fig_dir.add_trace(
            go.Scatter(x=[None], y=[None], mode="markers", marker=dict(color="green", size=10, symbol="star"), name="Peak")
        )
        fig_dir.add_trace(
            go.Scatter(x=[None], y=[None], mode="lines", line=dict(color="blue"), name="Wind Speed (m/s)")
        )
        fig_dir.add_trace(
            go.Scatter(x=[None], y=[None], mode="lines", line=dict(color="red"), name="Gust Wind Speed (m/s)")
        )

        st.plotly_chart(fig_dir, use_container_width=True)
    
         # ---------------- Temperature Plot ----------------
temp_col = "8. Air Temp (C)"
if temp_col in plot_df.columns:
    # Convert to numeric safely
    plot_df[temp_col] = pd.to_numeric(plot_df[temp_col], errors="coerce")
    filtered_df[temp_col] = pd.to_numeric(filtered_df[temp_col], errors="coerce")

    if not plot_df[temp_col].isna().all():
        fig_temp = px.line(
            plot_df,
            x="Time", y=temp_col, color="Date",
            title="Air Temperature Over The Time (by Date)",
            markers=True
        )
        fig_temp.update_xaxes(dtick=4)  # every 2 hours
        fig_temp.update_yaxes(title="Temperature (°C)")

        st.plotly_chart(fig_temp, use_container_width=True)

        # 👉 Temperature stats
        avg_temp = filtered_df[temp_col].mean(skipna=True)
        max_temp = filtered_df[temp_col].max(skipna=True)
        min_temp = filtered_df[temp_col].min(skipna=True)

        st.markdown(
            f"""
            <div style="background-color:#fff0e6; padding:10px; border-radius:8px; border:1px solid #ffb380;
                        width:fit-content; margin-top:-5px;">
            <b>Temperature Summary</b><br>
            🌡️ <b>Average:</b> {avg_temp:.2f} °C, <b>Max:</b> {max_temp:.2f} °C, <b>Min:</b> {min_temp:.2f} °C
            </div>
            """,
            unsafe_allow_html=True
        )


        # ---------------- Solar Radiation Plot ----------------
solar_col = "1.Solar (W/m2)"
if solar_col in plot_df.columns:
    # Convert safely
    plot_df[solar_col] = pd.to_numeric(plot_df[solar_col], errors="coerce")
    filtered_df[solar_col] = pd.to_numeric(filtered_df[solar_col], errors="coerce")

    if not plot_df[solar_col].isna().all():
        fig_solar = px.line(
            plot_df,
            x="Time", y=solar_col, color="Date",
            title="Solar Radiation Over Time (by Date)",
            markers=True
        )
        fig_solar.update_xaxes(dtick=4)  # every 2 hours
        fig_solar.update_yaxes(title="Solar Radiation (W/m²)")

        st.plotly_chart(fig_solar, use_container_width=True)

        if solar_col in filtered_df.columns:
           sunrise_time = None
           sunset_time = None
           threshold = 10  # W/m²

        above_threshold = filtered_df[filtered_df[solar_col] > threshold]

        if not above_threshold.empty:
         sunrise_time = above_threshold["Time"].iloc[0]
         sunset_time = above_threshold["Time"].iloc[-1]

        st.markdown(
        f"""
        <div style="background-color:#e6f7ff; padding:10px; border-radius:8px; border:1px solid #99ddff;
                    width:fit-content; margin-top:-5px;">
        🌄 <b>Sunrise:</b> {sunrise_time if sunrise_time else "Not detected"} <br>
        🌇 <b>Sunset:</b> {sunset_time if sunset_time else "Not detected"}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- Relative Humidity Plot ----------------
    rh_col = "11. RH (in Fractio)"

    if rh_col in plot_df.columns:
    # Convert fraction to percentage
      plot_df[rh_col] = pd.to_numeric(plot_df[rh_col], errors="coerce") * 100
      filtered_df[rh_col] = pd.to_numeric(filtered_df[rh_col], errors="coerce") * 100

    # Rename column for clarity in plots and table
      plot_df.rename(columns={rh_col: "11. RH (%)"}, inplace=True)
      filtered_df.rename(columns={rh_col: "11. RH (%)"}, inplace=True)
      rh_col = "11. RH (%)"  # update reference

      fig_rh = px.line(
        plot_df,
        x="Time",
        y=rh_col,
        color="Date",
        title="Relative Humidity Over Time (by Date)",
        markers=True
    )
      fig_rh.update_traces(mode="lines+markers")
      fig_rh.update_layout(
        yaxis_title="Relative Humidity (%)",
        xaxis_title="Time"
    )
      fig_rh.update_xaxes(dtick=4)
      st.plotly_chart(fig_rh, use_container_width=True)

    # ---------------- Vapor Pressure Plot ----------------
    vp_col = "9. Vapor Pressure (kPa)"

    if vp_col in plot_df.columns:
     plot_df[vp_col] = pd.to_numeric(plot_df[vp_col], errors="coerce")
     filtered_df[vp_col] = pd.to_numeric(filtered_df[vp_col], errors="coerce")

     fig_vp = px.line(
        plot_df,
        x="Time",
        y=vp_col,
        color="Date",
        title="Vapor Pressure Over Time (by Date)",
        markers=True
    )
     fig_vp.update_traces(mode="lines+markers")
     fig_vp.update_layout(
        yaxis_title="Vapor Pressure (kPa)",
        xaxis_title="Time"
    )
     fig_vp.update_xaxes(dtick=4)
     st.plotly_chart(fig_vp, use_container_width=True)

     st.subheader("📊 Correlation Analysis")

# Pick only the relevant numeric columns
     corr_cols = [
     "2.Percipitation (mm)",
     "11. RH (%)",
     "9. Vapor Pressure (kPa)",
     "8. Air Temp (C)",
     "1.Solar (W/m2)",
     "5. Wind Speed (m/s)",
     "18. Gust Wind Speed (m/s)"
]

# Ensure numeric
    corr_df = filtered_df[corr_cols].apply(pd.to_numeric, errors="coerce")

# Drop rows where all are NaN
    corr_df = corr_df.dropna(how="all")

    if not corr_df.empty:
     corr_matrix = corr_df.corr(method="pearson")

    # Plot heatmap
     fig, ax = plt.subplots(figsize=(5, 5))
     sns.heatmap(
        corr_matrix, 
        annot=True, fmt=".2f", cmap="coolwarm", 
        vmin=-1, vmax=1, cbar=True, ax=ax
    )
     ax.set_title("Correlation Heatmap", fontsize=14, pad=12)
     st.pyplot(fig)

     # ---------------- Scatter Plot for Relationships ----------------
     st.subheader("🔍 Explore Variable Relationships with Precipitation")

 # Dropdowns for variable selection
    options = [
     "8. Air Temp (C)",
     "1.Solar (W/m2)",
     "11. RH (%)",
     "9. Vapor Pressure (kPa)",
     "5. Wind Speed (m/s)",
     "18. Gust Wind Speed (m/s)"
]

    x_var = st.selectbox("Select Variable (X-axis)", options)

# Ensure numeric
    scatter_df = filtered_df.copy()
    scatter_df[x_var] = pd.to_numeric(scatter_df[x_var], errors="coerce")
    scatter_df["2.Percipitation (mm)"] = pd.to_numeric(scatter_df["2.Percipitation (mm)"], errors="coerce")

    if not scatter_df[[x_var, "2.Percipitation (mm)"]].dropna().empty:
     fig_scatter = px.scatter(
        scatter_df,
        x=x_var,
        y="2.Percipitation (mm)",
        color="Date",
        trendline="ols",
        title=f"Precipitation vs {x_var}"
    )
     st.plotly_chart(fig_scatter, use_container_width=True)


# --- Dropdown options ---
options = [
    "8. Air Temp (C)",
    "1.Solar (W/m2)",
    "2.Percipitation (mm)",
    "11. RH (%)",
    "9. Vapor Pressure (kPa)",
    "5. Wind Speed (m/s)",
    "18. Gust Wind Speed (m/s)"
]

######-------------Multi-Variable Time Series---------####################

# --- UI for variable selection ---
selected_vars = st.multiselect(
    "📊 Select variables to compare",
    options=options,
    default=["8. Air Temp (C)", "11. RH (%)"]
)

if selected_vars:
    filtered_df["DateTime"] = pd.to_datetime(filtered_df["Date"].astype(str) + " " + filtered_df["Time"].astype(str))
    filtered_df["OnlyTime"] = filtered_df["DateTime"].dt.strftime("%H:%M")

    fig = go.Figure()

    # First variable → main y-axis
    fig.add_trace(go.Scatter(
        x=filtered_df["DateTime"],
        y=filtered_df[selected_vars[0]],
        mode="lines",
        name=selected_vars[0],
        yaxis="y1"
    ))

    # Other variables → extra y-axes
    for i, var in enumerate(selected_vars[1:], start=2):
        fig.add_trace(go.Scatter(
            x=filtered_df["DateTime"],
            y=filtered_df[var],
            mode="lines",
            name=var,
            yaxis=f"y{i}"
        ))
        fig.update_layout({f"yaxis{i}": dict(
            title=var,
            overlaying="y1",
            side="right",
            showgrid=False,
            position=1 - (i-2)*0.05
        )})

    # Layout with main x-axis (time)
    fig.update_layout(
        title="Multi-Variable Time Series",
        xaxis=dict(
            title="Time of Day",
            tickformat="%H:%M",
            showgrid=True,
            title_standoff=30
        ),
        yaxis=dict(title=selected_vars[0]),
        legend=dict(orientation="v", y=0, x=7),
        width=1500,
        height=500,
        margin=dict(l=60, r=60, t=50, b=120),
        hovermode="x unified",  # unified hover
        hoverlabel=dict(bgcolor="white", font_size=12, font_family="Arial")
    )

    # Add date labels as annotations under x-axis
    for d, sub in filtered_df.groupby("Date"):
        mid_time = sub["DateTime"].iloc[len(sub)//2]
        fig.add_annotation(
            x=mid_time,
            y=-0.15,  # below x-axis
            text=str(d),
            showarrow=False,
            xref="x",
            yref="paper",
            align="center",
            font=dict(size=12)
        )

    st.plotly_chart(fig, use_container_width=False)




# # --- Dropdown options ---
# options = [
#     "8. Air Temp (C)",
#     "1.Solar (W/m2)",
#     "11. RH (%)",
#     "9. Vapor Pressure (kPa)",
#     "5. Wind Speed (m/s)",
#     "18. Gust Wind Speed (m/s)"
# ]

# # --- UI for variable selection ---
# selected_vars = st.multiselect(
#     "📊 Select variables to compare",
#     options=options,
#     default=["8. Air Temp (C)", "11. RH (%)"]
# )

# if selected_vars:
#     # Combine Date + Time into full datetime
#     filtered_df["DateTime"] = pd.to_datetime(
#         filtered_df["Date"].astype(str) + " " + filtered_df["Time"].astype(str)
#     )
#     filtered_df = filtered_df.sort_values("DateTime").reset_index(drop=True)

#     # --- OPTIONAL: make sure every variable has a value at the same timestamps.
#     # If your dataset already has identical timestamps for all variables you can skip this.
#     # This resamples to the minimum interval present and interpolates missing values:
#     # Uncomment if traces disappear on hover because timestamps don't match exactly.
#     # min_delta = filtered_df["DateTime"].diff().dropna().min()
#     # freq = pd.infer_freq(filtered_df["DateTime"]) or f"{int(min_delta.total_seconds()/60)}T"
#     # df_ts = filtered_df.set_index("DateTime").resample(freq).interpolate(method="time").reset_index()
#     # filtered_df = df_ts

#     # Create stacked subplots with shared x-axis
#     fig = make_subplots(
#         rows=len(selected_vars),
#         cols=1,
#         shared_xaxes=True,
#         vertical_spacing=0.03,
#         subplot_titles=selected_vars
#     )

#     # Add each variable as a separate subplot trace
#     for i, var in enumerate(selected_vars, start=1):
#         fig.add_trace(
#             go.Scatter(
#                 x=filtered_df["DateTime"],
#                 y=filtered_df[var],
#                 mode="lines",
#                 name=var,
#                 # keep hovertemplate simple so the unified hover prints nicely
#                 hovertemplate=f"{var}: %{{y:.3f}}<br>Time: %{{x|%Y-%m-%d %H:%M}}<extra></extra>"
#             ),
#             row=i,
#             col=1
#         )

#     # Explicitly match all x-axes so hovermode='x unified' works reliably
#     fig.update_xaxes(matches="x")

#     # show vertical spike line across subplots and snap to cursor
#     fig.update_xaxes(showspikes=True, spikesnap="cursor", spikemode="across", spikecolor="grey")
#     fig.update_layout(spikedistance=1000, hoverdistance=100)

#     # Add date labels as annotations under the bottom x-axis (optional)
#     for d, sub in filtered_df.groupby("Date"):
#         mid_time = sub["DateTime"].iloc[len(sub)//2]
#         fig.add_annotation(
#             x=mid_time,
#             y=-0.12,  # below the plots (paper coords)
#             text=str(d),
#             showarrow=False,
#             xref="x",
#             yref="paper",
#             align="center",
#             font=dict(size=11)
#         )

#     # Layout: unified hover, legend fixed at bottom, margins to fit annotations
#     fig.update_layout(
#         height=280 * len(selected_vars),
#         width=1000,
#         title="Stacked Multi-Variable Time Series",
#         hovermode="x unified",               # <--- THIS makes hover show all traces' values
#         showlegend=True,
#         legend=dict(orientation="h", y=-0.18),
#         margin=dict(l=80, r=80, t=60, b=140),
#         hoverlabel=dict(bgcolor="white", font_size=12)
#     )

#     # Update axis labels
#     fig.update_xaxes(title_text="Time of Day", tickformat="%H:%M")
#     for i, var in enumerate(selected_vars, start=1):
#         fig.update_yaxes(title_text=var, row=i, col=1)

#     st.plotly_chart(fig, use_container_width=True)

# else:
#     st.warning("⚠️ Select at least one variable to display.")

# else:
#     st.warning("⚠️ Not enough valid data for scatter plot.")
 
# else:
#     st.warning("⚠️ Not enough data to compute correlations.")
    
    # else:
    #     st.warning("⚠️ No wind data available for the selected date range.")

    # ---------------- Data Table ----------------
    st.subheader("📊 Filtered Data")
    st.dataframe(filtered_df)

else:
    st.warning("⚠️ No data available for the selected date range.")
















































