import streamlit as st
import plotly.express as px
import pandas as pd

from utils import load_data, sidebar_filters

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Stay Duration Analysis",
    page_icon="🛏️",
    layout="wide"
)

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

df = load_data()
df = sidebar_filters(df)

# Calculate Total Stay
df["total_stay"] = (
    df["stays_in_weekend_nights"] +
    df["stays_in_weekdays_nights"]
)

st.title("🛏️ Stay Duration Analysis")

st.markdown("""
Analyze how guest stay duration affects booking behaviour,
hotel performance and cancellation rate.
""")

# -------------------------------------------------------
# KPI Cards
# -------------------------------------------------------

avg_stay = round(df["total_stay"].mean(), 2)
max_stay = df["total_stay"].max()
min_stay = df["total_stay"].min()

long_stay = len(df[df["total_stay"] >= 7])

c1, c2, c3, c4 = st.columns(4)

c1.metric("Average Stay", f"{avg_stay} Nights")
c2.metric("Maximum Stay", f"{max_stay} Nights")
c3.metric("Minimum Stay", f"{min_stay} Night")
c4.metric("Long Stay Bookings", long_stay)

st.divider()

# -------------------------------------------------------
# Stay Distribution
# -------------------------------------------------------

fig = px.histogram(
    df,
    x="total_stay",
    nbins=30,
    color="hotel",
    title="Distribution of Stay Duration"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------
# Weekend vs Weekday Stay
# -------------------------------------------------------

stay = pd.DataFrame({
    "Stay Type": ["Weekend Nights", "Week Nights"],
    "Average Nights": [
        df["stays_in_weekend_nights"].mean(),
        df["stays_in_weekdays_nights"].mean()
    ]
})

fig = px.bar(
    stay,
    x="Stay Type",
    y="Average Nights",
    color="Stay Type",
    text_auto=".2f",
    title="Average Weekend vs Weekday Stay"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------------
# Stay Duration by Hotel
# -------------------------------------------------------

fig = px.box(
    df,
    x="hotel",
    y="total_stay",
    color="hotel",
    title="Stay Duration by Hotel Type"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------
# Stay Duration Categories
# -------------------------------------------------------

bins = [0, 2, 5, 10, 20, 100]
labels = [
    "1-2 Nights",
    "3-5 Nights",
    "6-10 Nights",
    "11-20 Nights",
    "20+ Nights"
]

df["Stay Category"] = pd.cut(
    df["total_stay"],
    bins=bins,
    labels=labels
)

stay_cat = (
    df.groupby("Stay Category")
    .size()
    .reset_index(name="Bookings")
)

fig = px.bar(
    stay_cat,
    x="Stay Category",
    y="Bookings",
    color="Bookings",
    text="Bookings",
    title="Bookings by Stay Category"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------------
# Cancellation Rate by Stay
# -------------------------------------------------------

cancel = (
    df.groupby("Stay Category")["is_canceled"]
    .mean()
    .reset_index()
)

cancel["Cancellation Rate"] = (
    cancel["is_canceled"] * 100
).round(2)

fig = px.bar(
    cancel,
    x="Stay Category",
    y="Cancellation Rate",
    color="Cancellation Rate",
    text="Cancellation Rate",
    title="Cancellation Rate by Stay Category"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------
# Average Stay by Month
# -------------------------------------------------------

monthly = (
    df.groupby("arrival_date_month")["total_stay"]
    .mean()
    .reset_index()
)

fig = px.line(
    monthly,
    x="arrival_date_month",
    y="total_stay",
    markers=True,
    title="Average Stay Duration by Month"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------------
# Market Segment
# -------------------------------------------------------

segment = (
    df.groupby("market_segment")["total_stay"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    segment,
    x="market_segment",
    y="total_stay",
    color="total_stay",
    title="Average Stay by Market Segment"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------
# Customer Type
# -------------------------------------------------------

customer = (
    df.groupby("customer_type")["total_stay"]
    .mean()
    .reset_index()
)

fig = px.bar(
    customer,
    x="customer_type",
    y="total_stay",
    color="total_stay",
    title="Average Stay by Customer Type"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------------
# Stay vs ADR
# -------------------------------------------------------

sample = df.sample(min(len(df), 4000), random_state=42)

fig = px.scatter(
    sample,
    x="total_stay",
    y="adr",
    color="hotel",
    size="lead_time",
    title="Stay Duration vs ADR"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------
# Hotel-wise Average Stay
# -------------------------------------------------------

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

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------------
# Heatmap
# -------------------------------------------------------

heat = (
    df.groupby(["arrival_date_month", "hotel"])
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
    text_auto=".2f",
    aspect="auto",
    color_continuous_scale="Viridis",
    title="Average Stay Duration Heatmap"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------------
# Summary Table
# -------------------------------------------------------

summary = (
    df.groupby("hotel")
    .agg(
        Average_Stay=("total_stay", "mean"),
        Maximum_Stay=("total_stay", "max"),
        Minimum_Stay=("total_stay", "min"),
        Total_Bookings=("hotel", "count")
    )
    .reset_index()
)

st.subheader("📋 Stay Duration Summary")

st.dataframe(summary, use_container_width=True)

st.divider()

# -------------------------------------------------------
# Business Insights
# -------------------------------------------------------

highest_segment = (
    segment.sort_values(
        "total_stay",
        ascending=False
    )
    .iloc[0]["market_segment"]
)

highest_customer = (
    customer.sort_values(
        "total_stay",
        ascending=False
    )
    .iloc[0]["customer_type"]
)

highest_month = (
    monthly.sort_values(
        "total_stay",
        ascending=False
    )
    .iloc[0]["arrival_date_month"]
)

st.subheader("📌 Business Insights")

st.success(f"""
🏨 Average Stay Duration: **{avg_stay} Nights**

📅 Highest Average Stay Month: **{highest_month}**

💼 Longest Stay Market Segment: **{highest_segment}**

👥 Longest Stay Customer Type: **{highest_customer}**

🌙 Long stays contribute significantly to hotel occupancy and revenue.
""")

# -------------------------------------------------------
# Recommendations
# -------------------------------------------------------

st.subheader("💡 Business Recommendations")

st.info("""
### Recommendation 1
Offer discounts for extended stays to improve occupancy.

### Recommendation 2
Create long-stay packages including meals and additional services.

### Recommendation 3
Provide loyalty benefits for guests staying more than one week.

### Recommendation 4
Target business travelers and families with customized stay plans.

### Recommendation 5
Monitor long-stay bookings as they have a greater impact on occupancy and revenue planning.

### Recommendation 6
Bundle room upgrades and complimentary services to encourage longer stays.
""")