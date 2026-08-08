import streamlit as st
import plotly.express as px
import pandas as pd

from utils import load_data, sidebar_filters

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Customer Analysis",
    page_icon="👥",
    layout="wide"
)

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

df = load_data()
df = sidebar_filters(df)

st.title("👥 Customer Analysis")

st.markdown("""
Analyze customer demographics, guest types, booking behavior,
countries, meal preferences, room preferences, and repeat guests.
""")

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

total_guest = len(df)

repeated = df["is_repeated_guest"].sum()

new_guest = total_guest - repeated

repeat_rate = round((repeated / total_guest) * 100, 2)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Bookings", f"{total_guest:,}")
c2.metric("New Guests", new_guest)
c3.metric("Repeated Guests", repeated)
c4.metric("Repeat Rate", f"{repeat_rate}%")

st.divider()

# ---------------------------------------------------
# Customer Type
# ---------------------------------------------------

customer = (
    df["customer_type"]
    .value_counts()
    .reset_index()
)

customer.columns = ["Customer Type", "Bookings"]

fig = px.pie(
    customer,
    names="Customer Type",
    values="Bookings",
    hole=0.45,
    title="Customer Type Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Repeated Guests
# ---------------------------------------------------

repeat = (
    df["is_repeated_guest"]
    .value_counts()
    .reset_index()
)

repeat.columns = ["Repeated", "Bookings"]

repeat["Repeated"] = repeat["Repeated"].map(
    {
        0: "New Guest",
        1: "Repeated Guest"
    }
)

fig = px.bar(
    repeat,
    x="Repeated",
    y="Bookings",
    color="Repeated",
    text="Bookings",
    title="Repeated Guests"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------
# Market Segment
# ---------------------------------------------------

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

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------
# Meal Preference
# ---------------------------------------------------

meal = (
    df["meal"]
    .value_counts()
    .reset_index()
)

meal.columns = [
    "Meal",
    "Bookings"
]

fig = px.pie(
    meal,
    names="Meal",
    values="Bookings",
    hole=.45,
    title="Meal Preference"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Adults Children Babies
# ---------------------------------------------------

family = pd.DataFrame({
    "Category": [
        "Adults",
        "Children",
        "Babies"
    ],
    "Count": [
        df["adults"].sum(),
        df["children"].sum(),
        df["babies"].sum()
    ]
})

fig = px.bar(
    family,
    x="Category",
    y="Count",
    color="Category",
    text="Count",
    title="Guest Composition"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Booking Channel
# ---------------------------------------------------

channel = (
    df["distribution_channel"]
    .value_counts()
    .reset_index()
)

channel.columns = [
    "Channel",
    "Bookings"
]

fig = px.bar(
    channel,
    x="Channel",
    y="Bookings",
    color="Bookings",
    title="Distribution Channel"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------
# Customer Type by Hotel
# ---------------------------------------------------

hotel_customer = (
    df.groupby(
        ["hotel", "customer_type"]
    )
    .size()
    .reset_index(name="Bookings")
)

fig = px.bar(
    hotel_customer,
    x="customer_type",
    y="Bookings",
    color="hotel",
    barmode="group",
    title="Customer Type by Hotel"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# Heatmap
# ---------------------------------------------------

heat = (
    df.groupby(
        ["customer_type", "hotel"]
    )
    .size()
    .reset_index(name="Bookings")
)

pivot = heat.pivot(
    index="customer_type",
    columns="hotel",
    values="Bookings"
)

fig = px.imshow(
    pivot,
    text_auto=True,
    aspect="auto",
    color_continuous_scale="Blues",
    title="Customer Type Heatmap"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------------------------
# Business Summary
# ---------------------------------------------------

top_customer = (
    df["customer_type"]
    .value_counts()
    .idxmax()
)

top_market = (
    df["market_segment"]
    .value_counts()
    .idxmax()
)

top_meal = (
    df["meal"]
    .value_counts()
    .idxmax()
)

st.subheader("📌 Business Insights")

st.success(f"""
👥 Most Common Customer Type: **{top_customer}**

# 🌍 Top Booking Country: **{"top_country"}**

🍽 Most Preferred Meal Plan: **{top_meal}**

🛏 Most Reserved Room Type: **{"top_room"}**

💼 Largest Market Segment: **{top_market}**

🔄 Repeat Guest Rate: **{repeat_rate}%**
""")

# ---------------------------------------------------
# Recommendations
# ---------------------------------------------------

st.subheader("💡 Business Recommendations")

st.info("""
### Recommendation 1
Increase loyalty rewards to improve repeat guest bookings.

### Recommendation 2
Offer personalized packages for the most common customer type.

### Recommendation 3
Promote premium room upgrades during the booking process.

### Recommendation 4
Focus international marketing campaigns on countries generating the highest number of bookings.

### Recommendation 5
Customize meal packages based on customer preferences.

### Recommendation 6
Strengthen partnerships with high-performing distribution channels.

### Recommendation 7
Use customer segmentation to create targeted marketing campaigns and improve guest satisfaction.
""")