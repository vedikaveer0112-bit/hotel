import streamlit as st
import plotly.express as px
import pandas as pd

from utils import load_data, sidebar_filters

# -------------------------------------------------------
# Page Config
# -------------------------------------------------------

st.set_page_config(
    page_title="Revenue Analysis",
    page_icon="💰",
    layout="wide"
)

# -------------------------------------------------------
# Load Data
# -------------------------------------------------------

df = load_data()
df = sidebar_filters(df)

st.title("💰 Revenue & ADR Analysis")

st.markdown("""
Analyze Average Daily Rate (ADR), estimated revenue,
revenue loss due to cancellations, pricing trends,
and hotel profitability.
""")

# -------------------------------------------------------
# Revenue Calculation
# -------------------------------------------------------

df["Revenue"] = df["adr"] * df["total_stay"]

confirmed = df[df["is_canceled"] == 0]
cancelled = df[df["is_canceled"] == 1]

total_revenue = confirmed["Revenue"].sum()
lost_revenue = cancelled["Revenue"].sum()

avg_adr = round(df["adr"].mean(), 2)
max_adr = round(df["adr"].max(), 2)

# -------------------------------------------------------
# KPI Cards
# -------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Revenue", f"${total_revenue:,.0f}")
c2.metric("Revenue Lost", f"${lost_revenue:,.0f}")
c3.metric("Average ADR", f"${avg_adr}")
c4.metric("Maximum ADR", f"${max_adr}")

st.divider()

# -------------------------------------------------------
# Revenue by Hotel
# -------------------------------------------------------

hotel = (
    confirmed.groupby("hotel")["Revenue"]
    .sum()
    .reset_index()
)

fig = px.bar(
    hotel,
    x="hotel",
    y="Revenue",
    color="hotel",
    text_auto=".2s",
    title="Revenue by Hotel Type"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------
# Revenue by Month
# -------------------------------------------------------

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
    title="Monthly Revenue Trend"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------------
# ADR Distribution
# -------------------------------------------------------

fig = px.histogram(
    df,
    x="adr",
    nbins=50,
    color="hotel",
    title="Average Daily Rate Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------
# ADR by Hotel
# -------------------------------------------------------

fig = px.box(
    df,
    x="hotel",
    y="adr",
    color="hotel",
    title="ADR by Hotel Type"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------------
# Revenue Loss by Hotel
# -------------------------------------------------------

loss = (
    cancelled.groupby("hotel")["Revenue"]
    .sum()
    .reset_index()
)

fig = px.bar(
    loss,
    x="hotel",
    y="Revenue",
    color="hotel",
    text_auto=".2s",
    title="Revenue Lost due to Cancellation"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------
# Revenue by Market Segment
# -------------------------------------------------------

segment = (
    confirmed.groupby("market_segment")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig = px.bar(
    segment,
    x="market_segment",
    y="Revenue",
    color="Revenue",
    title="Revenue by Market Segment"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------------
# Revenue by Customer Type
# -------------------------------------------------------

customer = (
    confirmed.groupby("customer_type")["Revenue"]
    .sum()
    .reset_index()
)

fig = px.pie(
    customer,
    names="customer_type",
    values="Revenue",
    hole=0.45,
    title="Revenue Contribution by Customer Type"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------
# ADR by Month
# -------------------------------------------------------

adr_month = (
    df.groupby("arrival_date_month")["adr"]
    .mean()
    .reset_index()
)

fig = px.line(
    adr_month,
    x="arrival_date_month",
    y="adr",
    markers=True,
    title="Average Daily Rate by Month"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------------
# Revenue Heatmap
# -------------------------------------------------------

heat = (
    confirmed.groupby(["arrival_date_month", "hotel"])["Revenue"]
    .sum()
    .reset_index()
)

pivot = heat.pivot(
    index="arrival_date_month",
    columns="hotel",
    values="Revenue"
)

fig = px.imshow(
    pivot,
    text_auto=".2s",
    aspect="auto",
    color_continuous_scale="Greens",
    title="Monthly Revenue Heatmap"
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------
# Scatter Plot
# -------------------------------------------------------

sample = df.sample(min(len(df), 4000), random_state=42)

fig = px.scatter(
    sample,
    x="adr",
    y="Revenue",
    color="hotel",
    size="total_stay",
    hover_data=["market_segment"],
    title="ADR vs Revenue"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------------------------------
# Revenue Summary Table
# -------------------------------------------------------

summary = confirmed.groupby("hotel").agg(
    Bookings=("hotel", "count"),
    Revenue=("Revenue", "sum"),
    Average_ADR=("adr", "mean"),
    Average_Stay=("total_stay", "mean")
).reset_index()

st.subheader("📋 Revenue Summary")

st.dataframe(
    summary.style.format({
        "Revenue": "${:,.2f}",
        "Average_ADR": "${:.2f}",
        "Average_Stay": "{:.2f}"
    }),
    use_container_width=True
)

st.divider()

# -------------------------------------------------------
# Business Insights
# -------------------------------------------------------

top_hotel = hotel.sort_values(
    "Revenue",
    ascending=False
).iloc[0]["hotel"]

top_month = monthly.sort_values(
    "Revenue",
    ascending=False
).iloc[0]["arrival_date_month"]

top_segment = segment.iloc[0]["market_segment"]

loss_percent = round(
    (lost_revenue / (total_revenue + lost_revenue)) * 100,
    2
)

st.subheader("📌 Business Insights")

st.success(f"""
💰 Total Confirmed Revenue: **${total_revenue:,.0f}**

❌ Estimated Revenue Lost: **${lost_revenue:,.0f}**

📉 Revenue Loss Percentage: **{loss_percent}%**

🏨 Highest Revenue Hotel: **{top_hotel}**

📅 Highest Revenue Month: **{top_month}**

💼 Top Revenue Market Segment: **{top_segment}**
""")

# -------------------------------------------------------
# Recommendations
# -------------------------------------------------------

st.subheader("💡 Business Recommendations")

st.info("""
### Recommendation 1
Increase room prices during high-demand months using dynamic pricing.

### Recommendation 2
Focus marketing on the highest revenue-generating market segments.

### Recommendation 3
Reduce cancellations through deposits and reminder notifications.

### Recommendation 4
Offer premium packages to guests with longer stays.

### Recommendation 5
Improve occupancy during off-peak seasons with discounts and bundled offers.

### Recommendation 6
Monitor ADR regularly to balance competitiveness and profitability.

### Recommendation 7
Analyze high-value customers and implement loyalty programs to maximize repeat revenue.
""")