import streamlit as st
import plotly.express as px

from utils import (
    load_data,
    sidebar_filters,
    calculate_kpis,
    kpi_card,
    download_button
)

# -----------------------------------
# Page Config
# -----------------------------------

st.set_page_config(
    page_title="Home",
    page_icon="🏨",
    layout="wide"
)

# -----------------------------------
# Load Data
# -----------------------------------

df = load_data()

# Sidebar Filters
df = sidebar_filters(df)

# Calculate KPIs
kpis = calculate_kpis(df)

# -----------------------------------
# Title
# -----------------------------------

st.title("🏨 Hotel Business Dashboard")

st.markdown("""
### Investigating Hotel Booking Behaviour using Data Visualization

Analyze hotel bookings, cancellations, customer behaviour,
seasonality, stay duration, and revenue insights using
interactive dashboards.
""")

st.markdown("---")

# -----------------------------------
# KPI Cards
# -----------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    kpi_card("Total Bookings", f"{kpis['Bookings']:,}")

with col2:
    kpi_card("Cancelled", f"{kpis['Cancelled']:,}")

with col3:
    kpi_card(
        "Cancellation Rate",
        f"{kpis['Cancellation Rate']} %"
    )

col4, col5, col6 = st.columns(3)

with col4:
    kpi_card("Average ADR", f"${kpis['ADR']}")

with col5:
    kpi_card(
        "Average Lead Time",
        f"{kpis['Lead Time']} Days"
    )

with col6:
    kpi_card(
        "Average Stay",
        f"{kpis['Stay']} Nights"
    )

st.markdown("---")

# -----------------------------------
# Project Information
# -----------------------------------

left, right = st.columns([2, 1])

with left:

    st.subheader("📌 Business Problem")

    st.info("""
    Hotels experience frequent booking cancellations that affect
    revenue, occupancy, and resource planning.

    This dashboard helps identify:

    • Most popular hotel type

    • Booking trends

    • Cancellation behaviour

    • Customer booking patterns

    • Stay duration impact

    • Lead time impact
    """)

    st.subheader("🎯 Project Objectives")

    st.success("""
    ✔ Analyze hotel booking behaviour

    ✔ Understand cancellation trends

    ✔ Discover seasonal demand

    ✔ Improve hotel revenue

    ✔ Support business decision making
    """)

with right:

    st.image(
        "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=700",
        use_container_width=True
    )

st.markdown("---")

# -----------------------------------
# Dataset Overview
# -----------------------------------

st.subheader("📂 Dataset Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Rows", len(df))
c2.metric("Columns", len(df.columns))
c3.metric("Hotel Types", df["hotel"].nunique())

# Correct column = country
if "country" in df.columns:
    countries = df["country"].nunique()
elif "Country" in df.columns:
    countries = df["Country"].nunique()
else:
    countries = 0

c4.metric("Countries", countries)

st.write("### Sample Data")

st.dataframe(df.head())

download_button(df)

st.markdown("---")

# -----------------------------------
# Hotel Type Distribution
# -----------------------------------

col1, col2 = st.columns(2)

with col1:

    hotel = (
        df["hotel"]
        .value_counts()
        .reset_index()
    )

    hotel.columns = ["Hotel", "Bookings"]

    fig = px.pie(
        hotel,
        names="Hotel",
        values="Bookings",
        hole=0.45,
        title="Hotel Booking Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    cancel = (
        df["is_canceled"]
        .value_counts()
        .reset_index()
    )

    cancel.columns = ["Cancelled", "Count"]

    cancel["Cancelled"] = cancel["Cancelled"].map(
        {
            0: "Not Cancelled",
            1: "Cancelled"
        }
    )

    fig = px.pie(
        cancel,
        names="Cancelled",
        values="Count",
        hole=0.45,
        title="Booking Cancellation Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# -----------------------------------
# Monthly Booking Trend
# -----------------------------------

st.subheader("📈 Monthly Booking Trend")

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

monthly = (
    df.groupby("arrival_date_month")
    .size()
    .reindex(month_order)
    .reset_index(name="Bookings")
)

fig = px.line(
    monthly,
    x="arrival_date_month",
    y="Bookings",
    markers=True,
    title="Monthly Bookings"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.markdown("---")

# -----------------------------------
# Average Daily Rate
# -----------------------------------

left, right = st.columns(2)

with left:

    fig = px.box(
        df,
        x="hotel",
        y="adr",
        color="hotel",
        title="Average Daily Rate by Hotel"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.histogram(
        df,
        x="lead_time",
        nbins=40,
        title="Lead Time Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# -----------------------------------
# Booking Source
# -----------------------------------

left, right = st.columns(2)

with left:

    segment = (
        df["market_segment"]
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
        title="Bookings by Market Segment"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    customer = (
        df["customer_type"]
        .value_counts()
        .reset_index()
    )

    customer.columns = [
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

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

# -----------------------------------
# Business Insights
# -----------------------------------

st.subheader("💡 Quick Business Insights")

most_booked = (
    df["hotel"]
    .value_counts()
    .idxmax()
)

top_month = (
    df["arrival_date_month"]
    .value_counts()
    .idxmax()
)

cancel_rate = round(
    df["is_canceled"].mean() * 100,
    2
)

st.success(f"""
🏨 **Most Booked Hotel:** {most_booked}

📅 **Highest Booking Month:** {top_month}

❌ **Cancellation Rate:** {cancel_rate}%

📊 Use the pages on the left sidebar to perform detailed
analysis on booking behaviour, cancellations, stay duration,
lead time, revenue, and customer insights.
""")

st.markdown("---")

st.caption(
    "Hotel Business Dashboard | Streamlit • Plotly • Pandas"
)
