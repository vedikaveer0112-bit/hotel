import streamlit as st
import plotly.express as px
import pandas as pd

from utils import load_data, sidebar_filters

# ===================================================
# Page Config
# ===================================================

st.set_page_config(
    page_title="Stay Duration Analysis",
    page_icon="🛏️",
    layout="wide"
)

# ===================================================
# Load Data
# ===================================================

df = load_data()
df = sidebar_filters(df)

st.title("🛏️ Stay Duration Analysis")

st.markdown("""
Analyze how the length of stay influences booking behavior,
cancellations, customer preferences, and hotel performance.
""")

# ===================================================
# Create Total Stay
# ===================================================

df["total_stay"] = (
    df["stays_in_weekend_nights"] +
    df["stays_in_weekdays_nights"]
)

# ===================================================
# KPI Cards
# ===================================================

avg_stay = round(df["total_stay"].mean(),2)

longest = df["total_stay"].max()

shortest = df["total_stay"].min()

avg_weekend = round(df["stays_in_weekend_nights"].mean(),2)

c1,c2,c3,c4 = st.columns(4)

c1.metric("Average Stay",f"{avg_stay} Nights")
c2.metric("Longest Stay",longest)
c3.metric("Shortest Stay",shortest)
c4.metric("Weekend Avg",avg_weekend)

st.divider()

# ===================================================
# Stay Distribution
# ===================================================

fig = px.histogram(
    df,
    x="total_stay",
    nbins=30,
    title="Distribution of Total Stay",
    color_discrete_sequence=["royalblue"]
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ===================================================
# Hotel Wise Stay
# ===================================================

fig = px.box(
    df,
    x="hotel",
    y="total_stay",
    color="hotel",
    title="Stay Duration by Hotel Type"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ===================================================
# Stay vs Cancellation
# ===================================================

cancel = (
    df.groupby("total_stay")["is_canceled"]
    .mean()
    .reset_index()
)

cancel["Cancellation Rate"] = (
    cancel["is_canceled"]*100
).round(2)

fig = px.line(
    cancel,
    x="total_stay",
    y="Cancellation Rate",
    markers=True,
    title="Stay Duration vs Cancellation Rate"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ===================================================
# Weekend vs Week Nights
# ===================================================

stay = pd.DataFrame({
    "Stay Type":[
        "Weekend Nights",
        "Week Nights"
    ],
    "Average Nights":[
        df["stays_in_weekend_nights"].mean(),
        df["stays_in_weekdays_nights"].mean()
    ]
})

fig = px.bar(
    stay,
    x="Stay Type",
    y="Average Nights",
    color="Stay Type",
    title="Average Weekend vs Week Nights"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ===================================================
# Hotel Comparison
# ===================================================

hotel = (
    df.groupby("hotel")["total_stay"]
    .mean()
    .reset_index()
)

fig = px.bar(
    hotel,
    x="hotel",
    y="total_stay",
    color="hotel",
    text_auto=".2f",
    title="Average Stay by Hotel"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ===================================================
# Customer Type
# ===================================================

customer = (
    df.groupby("customer_type")["total_stay"]
    .mean()
    .reset_index()
)

fig = px.bar(
    customer,
    x="customer_type",
    y="total_stay",
    color="customer_type",
    title="Average Stay by Customer Type"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ===================================================
# Market Segment
# ===================================================

segment = (
    df.groupby("market_segment")["total_stay"]
    .mean()
    .reset_index()
)

fig = px.bar(
    segment,
    x="market_segment",
    y="total_stay",
    color="total_stay",
    title="Average Stay by Market Segment"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ===================================================
# Month Wise Stay
# ===================================================

month = (
    df.groupby("arrival_date_month")["total_stay"]
    .mean()
    .reset_index()
)

fig = px.line(
    month,
    x="arrival_date_month",
    y="total_stay",
    markers=True,
    title="Average Stay by Month"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ===================================================
# ADR vs Stay
# ===================================================

fig = px.scatter(
    df,
    x="total_stay",
    y="adr",
    color="hotel",
    opacity=0.6,
    title="ADR vs Stay Duration"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ===================================================
# Lead Time vs Stay
# ===================================================

fig = px.scatter(
    df,
    x="lead_time",
    y="total_stay",
    color="hotel",
    opacity=0.5,
    title="Lead Time vs Stay Duration"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ===================================================
# Heatmap
# ===================================================

heat = (
    df.groupby(["hotel","arrival_date_month"])
    ["total_stay"]
    .mean()
    .reset_index()
)

pivot = heat.pivot(
    index="arrival_date_month",
    columns="hotel",
    values="total_stay"
)

fig = px.imshow(
    pivot,
    text_auto=".1f",
    aspect="auto",
    color_continuous_scale="Viridis",
    title="Average Stay Heatmap"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ===================================================
# Insights
# ===================================================

highest_month = month.sort_values(
    "total_stay",
    ascending=False
).iloc[0]["arrival_date_month"]

highest_customer = customer.sort_values(
    "total_stay",
    ascending=False
).iloc[0]["customer_type"]

highest_segment = segment.sort_values(
    "total_stay",
    ascending=False
).iloc[0]["market_segment"]

hotel_name = hotel.sort_values(
    "total_stay",
    ascending=False
).iloc[0]["hotel"]

st.subheader("📌 Business Insights")

st.success(f"""
🏨 Hotel with Longest Stay: **{hotel_name}**

📅 Month with Longest Stay: **{highest_month}**

👤 Customer Type Staying Longest: **{highest_customer}**

💼 Market Segment with Longest Stay: **{highest_segment}**

🛏️ Average Stay Duration: **{avg_stay} Nights**
""")

# ===================================================
# Recommendations
# ===================================================

st.subheader("💡 Business Recommendations")

st.info("""
### Recommendation 1
Provide discounts for guests booking longer stays.

### Recommendation 2
Introduce long-stay packages with complimentary services.

### Recommendation 3
Offer loyalty rewards for extended bookings.

### Recommendation 4
Optimize housekeeping schedules based on average stay duration.

### Recommendation 5
Develop targeted marketing campaigns for customer segments that prefer longer stays.

### Recommendation 6
Create seasonal packages to encourage extended vacations during off-peak months.

### Recommendation 7
Monitor cancellation rates for long stays and consider flexible cancellation policies.
""")