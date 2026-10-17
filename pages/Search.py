import time
import streamlit as st
from utils import set_background, show_banner, show_nav, load_spots, get_recommendations

st.set_page_config(page_title="Search", page_icon="🐊", layout="wide")
set_background()
show_banner()
show_nav("Search")

st.markdown(
    """
    <style>
    .search-title {
        color: white;
        text-align: center;
        font-weight: 700;
    }
    </style>
    <h2 class="search-title">What are you craving? 🐊</h2>
    """,
    unsafe_allow_html=True,
)

prompt = st.chat_input("e.g. 15 min between classes near Reitz, I'm broke, need vegan")

if prompt:
    with st.spinner("🐊 Searching for Snacks..."):
        st.session_state.last_query = prompt
        st.session_state.last_results = get_recommendations(prompt, load_spots())
    st.switch_page("pages/Results.py")

