import streamlit as st
from utils import set_background, show_banner, show_nav

st.set_page_config(page_title="Results", page_icon="🐊", layout="wide")
set_background()
show_banner()
show_nav("Results")

st.markdown(
    """
    <style>
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(16px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        animation: fadeUp 0.5s ease-out both;
    }
    .results-heading { color: white; text-align: center; }
    </style>
    """,
    unsafe_allow_html=True,
)

query = st.session_state.get("last_query")
results = st.session_state.get("last_results")

if not results:
    st.markdown(
        "<h2 class='results-heading'>No search yet. Head to Search to find some food! 🐊</h2>",
        unsafe_allow_html=True,
    )
    st.stop()

st.markdown(f"<h3 class='results-heading'>Results for: <i>{query}</i></h3>", unsafe_allow_html=True)

for spot in results:
    with st.container(border=True):
        st.markdown(f"#### {spot['name']}")
        st.write(f"📍 {spot['nearest_landmark']}  ·  {spot['price_range']}  ·  {spot['speed'].replace('_', ' ')}")
        st.write(" ".join(f"`{t}`" for t in spot["tags"][:6]))
        st.link_button("Open in Google Maps", spot["google_maps_url"])