import streamlit as st
import plotly.express as px
import pandas as pd

from utils import load_data, sidebar_filters

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📈",
    layout="wide"
)

df = load_data()
df = sidebar_filters(df)

# --------------------------------------------------
# Calculations
# --------------------------------------------------

df["Revenue"] = df["adr"] * df["total_stay"]

confirmed = df[df["is_canceled"] == 0]
cancelled = df[df["is_canceled"] == 1]

total_bookings = len(df)
cancel_rate = round(df["is_canceled"].mean() * 100, 2)

total_revenue = confirmed["Revenue"].sum()
revenue_loss = cancelled["Revenue"].sum()

avg_adr = round(df["adr"].mean(), 2)
avg_lead = round(df["lead_time"].mean(), 1)
avg_stay = round(df["total_stay"].mean(), 1)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📈 Executive Business Dashboard")

st.markdown("""
A complete summary of hotel booking behaviour,
customer insights, cancellations,
lead time and revenue performance.
""")

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Bookings", f"{total_bookings:,}")
c2.metric("Cancellation Rate", f"{cancel_rate}%")
c3.metric("Revenue", f"${total_revenue:,.0f}")
c4.metric("Revenue Lost", f"${revenue_loss:,.0f}")

c5, c6, c7 = st.columns(3)

c5.metric("Average ADR", f"${avg_adr}")
c6.metric("Average Stay", f"{avg_stay} Days")
c7.metric("Average Lead Time", f"{avg_lead} Days")

st.divider()

# --------------------------------------------------
# Booking vs Cancellation
# --------------------------------------------------

left, right = st.columns(2)

with left:

    hotel = (
        df.hotel
        .value_counts()
        .reset_index()
    )

    hotel.columns = ["Hotel", "Bookings"]

    fig = px.pie(
        hotel,
        names="Hotel",
        values="Bookings",
        hole=.45,
        title="Booking Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    cancel = (
        df.groupby("hotel")["is_canceled"]
        .mean()
        .reset_index()
    )

    cancel["Cancellation Rate"] = (
        cancel["is_canceled"] * 100
    )

    fig = px.bar(
        cancel,
        x="hotel",
        y="Cancellation Rate",
        color="hotel",
        title="Cancellation Rate"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------------------------
# Monthly Revenue
# --------------------------------------------------

monthly = (
    confirmed.groupby("arrival_date_month")["Revenue"]
    .sum()
    .reset_index()
)

fig = px.line(
    monthly,
    x="arrival_date_month",
    y="Revenue",
    markers=True,
    title="Monthly Revenue"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# ADR vs Lead Time
# --------------------------------------------------

sample = df.sample(min(len(df), 4000), random_state=42)

fig = px.scatter(
    sample,
    x="lead_time",
    y="adr",
    color="hotel",
    size="total_stay",
    title="ADR vs Lead Time"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------------------------
# Market Segment
# --------------------------------------------------

segment = (
    df.market_segment
    .value_counts()
    .reset_index()
)

segment.columns = [
    "Market Segment",
    "Bookings"
]

fig = px.bar(
    segment,
    x="Market Segment",
    y="Bookings",
    color="Bookings",
    title="Market Segment Analysis"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# --------------------------------------------------
# Executive Summary
# --------------------------------------------------

st.header("📋 Executive Summary")

st.success(f"""
### Key Findings

• Total Bookings : {total_bookings:,}

• Overall Cancellation Rate : {cancel_rate}%

• Average Daily Rate : ${avg_adr}

• Average Stay Duration : {avg_stay} Days

• Average Lead Time : {avg_lead} Days

• Total Revenue : ${total_revenue:,.0f}

• Estimated Revenue Lost : ${revenue_loss:,.0f}
""")

# --------------------------------------------------
# Final Recommendations
# --------------------------------------------------

st.header("💡 Business Recommendations")

recommendations = pd.DataFrame({
    "Area":[
        "Pricing",
        "Cancellation",
        "Marketing",
        "Customer Loyalty",
        "Revenue",
        "Operations",
        "Forecasting"
    ],
    "Recommendation":[
        "Use dynamic pricing during peak seasons.",
        "Introduce deposits for high-risk bookings.",
        "Promote offers during off-season months.",
        "Launch loyalty rewards for repeat guests.",
        "Target high-value customer segments.",
        "Adjust staffing according to booking trends.",
        "Predict cancellations using machine learning."
    ]
})

st.dataframe(
    recommendations,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.header("🎯 Project Conclusion")

st.info("""
The dashboard shows that hotel performance is strongly influenced by seasonality,
lead time, customer segment and cancellation behaviour.

Hotels can significantly improve occupancy and profitability through
dynamic pricing, cancellation management, targeted marketing,
customer loyalty programs and predictive analytics.

This dashboard provides managers with actionable insights for
data-driven business decisions.
""")

st.caption("Hotel Business Dashboard | Executive Dashboard | Streamlit | Plotly")