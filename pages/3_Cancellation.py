import streamlit as st
import plotly.express as px
import pandas as pd

from utils import load_data, sidebar_filters

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------

st.set_page_config(
    page_title="Cancellation Analysis",
    page_icon="❌",
    layout="wide"
)

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

df = load_data()
df = sidebar_filters(df)

st.title("❌ Hotel Booking Cancellation Analysis")

st.markdown("""
Analyze booking cancellation behaviour across hotel type,
customer type, market segment, deposit type,
lead time and stay duration.
""")

# ===================================================
# KPI Cards
# ===================================================

total_booking = len(df)

cancelled = df[df["is_canceled"] == 1]

not_cancelled = df[df["is_canceled"] == 0]

cancel_rate = round((len(cancelled) / total_booking) * 100, 2)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Bookings", f"{total_booking:,}")
c2.metric("Cancelled", len(cancelled))
c3.metric("Confirmed", len(not_cancelled))
c4.metric("Cancellation Rate", f"{cancel_rate}%")

st.divider()

# ===================================================
# Hotel Cancellation
# ===================================================

left, right = st.columns(2)

with left:

    hotel_cancel = (
        df.groupby("hotel")["is_canceled"]
        .mean()
        .reset_index()
    )

    hotel_cancel["Cancellation Rate"] = (
        hotel_cancel["is_canceled"] * 100
    ).round(2)

    fig = px.bar(
        hotel_cancel,
        x="hotel",
        y="Cancellation Rate",
        color="hotel",
        text="Cancellation Rate",
        title="Cancellation Rate by Hotel"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    hotel_status = (
        df.groupby(["hotel", "is_canceled"])
        .size()
        .reset_index(name="Bookings")
    )

    hotel_status["Status"] = hotel_status["is_canceled"].map(
        {0: "Confirmed", 1: "Cancelled"}
    )

    fig = px.bar(
        hotel_status,
        x="hotel",
        y="Bookings",
        color="Status",
        barmode="group",
        title="Hotel Booking Status"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ===================================================
# Monthly Cancellation
# ===================================================

monthly = (
    df.groupby("arrival_date_month")["is_canceled"]
    .mean()
    .reset_index()
)

monthly["Cancellation Rate"] = (
    monthly["is_canceled"] * 100
).round(2)

fig = px.line(
    monthly,
    x="arrival_date_month",
    y="Cancellation Rate",
    markers=True,
    title="Monthly Cancellation Rate"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ===================================================
# Market Segment
# ===================================================

segment = (
    df.groupby("market_segment")["is_canceled"]
    .mean()
    .reset_index()
)

segment["Cancellation Rate"] = (
    segment["is_canceled"] * 100
).round(2)

fig = px.bar(
    segment,
    x="market_segment",
    y="Cancellation Rate",
    color="Cancellation Rate",
    title="Cancellation by Market Segment"
)

st.plotly_chart(fig, use_container_width=True)

# ===================================================
# Customer Type
# ===================================================

customer = (
    df.groupby("customer_type")["is_canceled"]
    .mean()
    .reset_index()
)

customer["Cancellation Rate"] = (
    customer["is_canceled"] * 100
).round(2)

fig = px.bar(
    customer,
    x="customer_type",
    y="Cancellation Rate",
    color="Cancellation Rate",
    title="Cancellation by Customer Type"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ===================================================
# Deposit Type
# ===================================================

deposit = (
    df.groupby("deposit_type")["is_canceled"]
    .mean()
    .reset_index()
)

deposit["Cancellation Rate"] = (
    deposit["is_canceled"] * 100
).round(2)

fig = px.bar(
    deposit,
    x="deposit_type",
    y="Cancellation Rate",
    color="Cancellation Rate",
    title="Cancellation by Deposit Type"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ===================================================
# Lead Time
# ===================================================

lead = (
    df.groupby(pd.cut(df["lead_time"], bins=10))
    ["is_canceled"]
    .mean()
    .reset_index()
)

lead["Cancellation Rate"] = (
    lead["is_canceled"] * 100
).round(2)

lead["Lead Time"] = lead["lead_time"].astype(str)

fig = px.line(
    lead,
    x="Lead Time",
    y="Cancellation Rate",
    markers=True,
    title="Cancellation vs Lead Time"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ===================================================
# Stay Duration
# ===================================================

stay = (
    df.groupby("total_stay")["is_canceled"]
    .mean()
    .reset_index()
)

stay["Cancellation Rate"] = (
    stay["is_canceled"] * 100
).round(2)

fig = px.line(
    stay,
    x="total_stay",
    y="Cancellation Rate",
    markers=True,
    title="Cancellation vs Stay Duration"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ===================================================
# Distribution
# ===================================================

left, right = st.columns(2)

with left:

    fig = px.histogram(
        cancelled,
        x="lead_time",
        nbins=40,
        title="Lead Time Distribution (Cancelled)"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    fig = px.histogram(
        cancelled,
        x="adr",
        nbins=40,
        title="ADR Distribution (Cancelled)"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ===================================================
# Heatmap
# ===================================================

heat = (
    df.groupby(["hotel", "arrival_date_month"])
    ["is_canceled"]
    .mean()
    .reset_index()
)

pivot = heat.pivot(
    index="arrival_date_month",
    columns="hotel",
    values="is_canceled"
)

fig = px.imshow(
    pivot,
    text_auto=".1%",
    aspect="auto",
    color_continuous_scale="Reds",
    title="Cancellation Heatmap"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ===================================================
# Business Insights
# ===================================================

highest_segment = (
    segment.sort_values(
        "Cancellation Rate",
        ascending=False
    )
    .iloc[0]["market_segment"]
)

highest_customer = (
    customer.sort_values(
        "Cancellation Rate",
        ascending=False
    )
    .iloc[0]["customer_type"]
)

highest_deposit = (
    deposit.sort_values(
        "Cancellation Rate",
        ascending=False
    )
    .iloc[0]["deposit_type"]
)

highest_month = (
    monthly.sort_values(
        "Cancellation Rate",
        ascending=False
    )
    .iloc[0]["arrival_date_month"]
)

st.subheader("📌 Business Insights")

st.success(f"""
• Overall Cancellation Rate : **{cancel_rate}%**

• Highest Cancellation Month : **{highest_month}**

• Highest Cancellation Segment : **{highest_segment}**

• Highest Cancellation Customer Type : **{highest_customer}**

• Highest Cancellation Deposit Type : **{highest_deposit}**
""")

# ===================================================
# Recommendations
# ===================================================

st.subheader("💡 Business Recommendations")

st.info("""
### Recommendation 1
Require advance deposits for bookings with long lead times.

### Recommendation 2
Send reminder emails and SMS notifications before arrival.

### Recommendation 3
Offer flexible rescheduling instead of direct cancellation.

### Recommendation 4
Provide loyalty discounts for repeat customers.

### Recommendation 5
Use dynamic cancellation policies during peak seasons.

### Recommendation 6
Closely monitor high-risk market segments and customer groups.

### Recommendation 7
Use predictive analytics to identify bookings with a high likelihood of cancellation.
""")