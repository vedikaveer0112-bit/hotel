import streamlit as st
import plotly.express as px
import pandas as pd

from utils import load_data, sidebar_filters

st.set_page_config(
    page_title="Booking Analysis",
    page_icon="📊",
    layout="wide"
)

# ==============================
# Load Data
# ==============================

df = load_data()
df = sidebar_filters(df)

st.title("📊 Booking Analysis")

st.markdown(
"""
This dashboard analyzes hotel booking behaviour,
monthly booking trends,
hotel popularity,
seasonality,
and booking distribution.
"""
)

# ============================================
# KPI Cards
# ============================================

total_booking = len(df)
city_booking = len(df[df.hotel=="City Hotel"])
resort_booking = len(df[df.hotel=="Resort Hotel"])

city_percent = round(city_booking/total_booking*100,2)
resort_percent = round(resort_booking/total_booking*100,2)

c1,c2,c3,c4 = st.columns(4)

c1.metric("Total Bookings",f"{total_booking:,}")
c2.metric("City Hotel",city_booking)
c3.metric("Resort Hotel",resort_booking)
c4.metric("City Booking %",f"{city_percent}%")

st.divider()

# ============================================
# Hotel Booking Share
# ============================================

left,right = st.columns(2)

with left:

    hotel = (
        df.hotel
        .value_counts()
        .reset_index()
    )

    hotel.columns=["Hotel","Bookings"]

    fig = px.pie(
        hotel,
        names="Hotel",
        values="Bookings",
        hole=.45,
        title="Booking Share by Hotel Type"
    )

    st.plotly_chart(fig,use_container_width=True)

with right:

    fig = px.bar(
        hotel,
        x="Hotel",
        y="Bookings",
        color="Hotel",
        text="Bookings",
        title="Hotel Booking Comparison"
    )

    st.plotly_chart(fig,use_container_width=True)

st.divider()

# ============================================
# Monthly Booking Trend
# ============================================

monthly = (
    df.groupby(
        ["arrival_date_month","hotel"]
    )
    .size()
    .reset_index(name="Bookings")
)

fig = px.line(
    monthly,
    x="arrival_date_month",
    y="Bookings",
    color="hotel",
    markers=True,
    title="Monthly Booking Trend by Hotel"
)

st.plotly_chart(fig,use_container_width=True)

# ============================================
# Booking by Month
# ============================================

month_total = (
    df.groupby("arrival_date_month")
    .size()
    .reset_index(name="Bookings")
)

fig = px.bar(
    month_total,
    x="arrival_date_month",
    y="Bookings",
    color="Bookings",
    text="Bookings",
    title="Total Monthly Bookings"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ============================================
# Booking by Year
# ============================================

year = (
    df.groupby(
        ["arrival_date_year","hotel"]
    )
    .size()
    .reset_index(name="Bookings")
)

fig = px.bar(
    year,
    x="arrival_date_year",
    y="Bookings",
    color="hotel",
    barmode="group",
    text="Bookings",
    title="Year Wise Booking Comparison"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ============================================
# Booking by Market Segment
# ============================================

segment = (
    df.market_segment
    .value_counts()
    .reset_index()
)

segment.columns=[
    "Market Segment",
    "Bookings"
]

fig = px.bar(
    segment,
    x="Market Segment",
    y="Bookings",
    color="Bookings",
    title="Bookings by Market Segment"
)

st.plotly_chart(fig,use_container_width=True)

# ============================================
# Customer Type
# ============================================

customer = (
    df.customer_type
    .value_counts()
    .reset_index()
)

customer.columns=[
    "Customer Type",
    "Bookings"
]

fig = px.bar(
    customer,
    x="Customer Type",
    y="Bookings",
    color="Bookings",
    title="Bookings by Customer Type"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ============================================
# Deposit Type
# ============================================

deposit = (
    df.deposit_type
    .value_counts()
    .reset_index()
)

deposit.columns=[
    "Deposit Type",
    "Bookings"
]

fig = px.pie(
    deposit,
    names="Deposit Type",
    values="Bookings",
    hole=.45,
    title="Booking by Deposit Type"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ============================================
# Reservation Status
# ============================================

status = (
    df.reservation_status
    .value_counts()
    .reset_index()
)

status.columns=[
    "Status",
    "Bookings"
]

fig = px.bar(
    status,
    x="Status",
    y="Bookings",
    color="Status",
    text="Bookings",
    title="Reservation Status"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ============================================
# Booking Heatmap
# ============================================

heat = (
    df.groupby(
        ["arrival_date_month","hotel"]
    )
    .size()
    .reset_index(name="Bookings")
)

pivot = heat.pivot(
    index="arrival_date_month",
    columns="hotel",
    values="Bookings"
)

fig = px.imshow(
    pivot,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues",
    title="Booking Heatmap"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ============================================
# Business Insights
# ============================================

most_booked = df.hotel.value_counts().idxmax()

highest_month = (
    df.arrival_date_month
    .value_counts()
    .idxmax()
)

lowest_month = (
    df.arrival_date_month
    .value_counts()
    .idxmin()
)

top_segment = (
    df.market_segment
    .value_counts()
    .idxmax()
)

st.subheader("📌 Business Insights")

st.success(f"""
🏨 Most Booked Hotel : **{most_booked}**

📅 Highest Booking Month : **{highest_month}**

📉 Lowest Booking Month : **{lowest_month}**

# 🌍 Highest Booking Country : **{"top_country"}**

💼 Largest Market Segment : **{top_segment}**
""")

# ============================================
# Recommendations
# ============================================

st.subheader("💡 Recommendations")

st.info("""
### Recommendation 1
Increase room prices during peak booking months using dynamic pricing.

### Recommendation 2
Launch promotional offers during low-demand months to improve occupancy.

### Recommendation 3
Target the largest market segment with personalized marketing campaigns.

### Recommendation 4
Strengthen international marketing in countries generating the highest bookings.

### Recommendation 5
Monitor seasonal demand trends to optimize staffing and inventory planning.
""")