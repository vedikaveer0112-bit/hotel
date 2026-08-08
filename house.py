import streamlit as st

st.set_page_config(
    page_title="Hotel Business Dashboard",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# Custom CSS
# -------------------------

st.markdown("""
<style>

[data-testid="stSidebar"]{
    background:#16325B;
}

[data-testid="stSidebar"] *{
    color:white;
}

.main{
    background:#F8F9FA;
}

.kpi{
    padding:20px;
    border-radius:12px;
    background:white;
    box-shadow:0px 0px 10px rgba(0,0,0,.10);
    text-align:center;
}

.big-font{
    font-size:35px;
    font-weight:bold;
}

.small-font{
    color:gray;
}

.footer{
    text-align:center;
    color:gray;
    padding-top:40px;
}

</style>
""", unsafe_allow_html=True)

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

st.markdown(
"""
<div class='footer'>
Developed using Streamlit • Plotly • Pandas
</div>
""",
unsafe_allow_html=True
)