import pandas as pd
import streamlit as st

# ----------------------------
# Load Dataset
# ----------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("hotel_bookings_data.csv")

    # Convert Date
    if "reservation_status_date" in df.columns:
        df["reservation_status_date"] = pd.to_datetime(
            df["reservation_status_date"]
        )

    # Total Stay
    df["total_stay"] = (
        df["stays_in_weekend_nights"] +
        df["stays_in_weekdays_nights"]
    )

    # Arrival Month Order

    months = [
        "January","February","March","April",
        "May","June","July","August",
        "September","October","November","December"
    ]

    if "arrival_date_month" in df.columns:

        df["arrival_date_month"] = pd.Categorical(
            df["arrival_date_month"],
            categories=months,
            ordered=True
        )

    return df


# ----------------------------------
# Sidebar Filters
# ----------------------------------

def sidebar_filters(df):

    st.sidebar.header("Filters")

    hotel = st.sidebar.multiselect(
        "Hotel Type",
        df.hotel.unique(),
        default=df.hotel.unique()
    )

    month = st.sidebar.multiselect(
        "Month",
        sorted(df.arrival_date_month.unique()),
        default=sorted(df.arrival_date_month.unique())
    )

    segment = st.sidebar.multiselect(
        "Market Segment",
        sorted(df.market_segment.unique()),
        default=sorted(df.market_segment.unique())
    )

    customer = st.sidebar.multiselect(
        "Customer Type",
        sorted(df.customer_type.unique()),
        default=sorted(df.customer_type.unique())
    )

    filtered = df[
        (df.hotel.isin(hotel))
        &
        (df.arrival_date_month.isin(month))
        &
        (df.market_segment.isin(segment))
        &
        (df.customer_type.isin(customer))
    ]

    return filtered


# ---------------------------------
# KPI Calculation
# ---------------------------------

def calculate_kpis(df):

    total_booking = len(df)

    cancelled = df["is_canceled"].sum()

    cancellation_rate = round(
        cancelled/total_booking*100,
        2
    )

    adr = round(df["adr"].mean(),2)

    lead = round(df["lead_time"].mean(),1)

    avg_stay = round(df["total_stay"].mean(),1)

    return {
        "Bookings":total_booking,
        "Cancelled":cancelled,
        "Cancellation Rate":cancellation_rate,
        "ADR":adr,
        "Lead Time":lead,
        "Stay":avg_stay
    }


# ----------------------------------
# KPI Card
# ----------------------------------

def kpi_card(title,value):

    st.markdown(
        f"""
        <div class='kpi'>
        <h3>{title}</h3>
        <h1>{value}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )


# -----------------------------------
# Download CSV
# -----------------------------------

def download_button(df):

    csv=df.to_csv(index=False).encode()

    st.download_button(
        label="⬇ Download Filtered Dataset",
        data=csv,
        file_name="filtered_hotel_data.csv",
        mime="text/csv"
    )