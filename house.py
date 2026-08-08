import streamlit as st

st.set_page_config(
    page_title="Hotel Business Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏨 Hotel Business Dashboard")

st.write("""
### Welcome

This dashboard analyzes hotel booking behaviour,
cancellation patterns,
stay duration,
lead time,
ADR,
and customer insights.

👈 Select a page from the sidebar.
""")

st.image(
    "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1200",
    use_container_width=True
)

st.markdown("---")
