import base64
import json
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).parent

@st.cache_data
def img_to_base64(path) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
@st.cache_data
def load_spots():
    with open(ROOT / "foodspots.json") as f:
        return json.load(f)


def set_background():
    encoded = img_to_base64(ROOT / "Uf_Reitz_Picture.jpg")

    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');

        html, body, [class*="css"], .stMarkdown, .stChatMessage, textarea, input, h1, h2, h3, h4 {{
            font-family: 'DM Sans', sans-serif !important;
        }}

        .stApp {{
            background-image:
                linear-gradient(rgba(0, 0, 0, 0.45), rgba(0, 0, 0, 0.45)),
                url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        [data-testid="stHeader"] {{
            background: transparent !important;
        }}

        [data-testid="stBottom"],
        [data-testid="stBottom"] > div,
        [data-testid="stBottomBlockContainer"] {{
            background: transparent !important;
        }}

        /* Hide the sidebar page list so users only navigate through the app */
        [data-testid="stSidebarNav"],
        [data-testid="stSidebar"],
        [data-testid="collapsedControl"] {{
            display: none !important;
        }}

        /* Hide the heading anchor-link icons */
        [data-testid="stHeaderActionElements"] {{
            display: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_banner():
    chef_gator = img_to_base64(ROOT / "gator_chef.png")

    st.markdown(
        f"""
        <style>
        .banner {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background-color: #0021A5;
            border: 3px solid #FA4616;
            border-radius: 32px;
            padding: 0.25rem 1.5rem;
            margin-top: -2rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }}
        .banner img {{
            height: 60px;
            width: 60px;
            object-fit: contain;
        }}
        .banner img.flip {{
            transform: scaleX(-1);
        }}
        .banner h1 {{
            flex: 1;
            text-align: center;
            color: white !important;
            font-family: 'DM Sans', sans-serif !important;
            font-weight: 700;
            font-size: 2.75rem;
            margin: 0;
            padding: 0;
        }}
        .banner h1 a {{
            display: none !important;
        }}
        .block-container {{
        padding-top: 3rem !important;
        }}
        </style>

        <div class="banner">
            <img src="data:image/png;base64,{chef_gator}">
            <h1>SwampSnacks</h1>
            <img class="flip" src="data:image/png;base64,{chef_gator}">
        </div>
        """,
        unsafe_allow_html=True,
    )

def show_nav(current: str):
    """Navigation bar under the banner. `current` is "Home", "Search", or "Results"."""
    pages = [
        ("Home", "FrontPage.py", "🏠"),
        ("Search", "pages/Search.py", "🔍"),
        ("Results", "pages/Results.py", "🍽️"),
    ]

    st.markdown(
        f"""
        <style>
        .st-key-navbar {{
            margin: 0.75rem auto 0.5rem;
        }}
        .st-key-navbar [data-testid="stPageLink"] a {{
            justify-content: center;
            background: rgba(255, 255, 255, 0.9);
            border: 2px solid transparent;
            border-radius: 999px;
            padding: 0.35rem 1rem;
            transition: background 0.2s, border-color 0.2s;
        }}
        .st-key-navbar [data-testid="stPageLink"] a:hover {{
            background: white;
            border-color: #FA4616;
        }}
        .st-key-navbar [data-testid="stPageLink"] a p {{
            color: #0021A5 !important;
            font-weight: 600;
        }}
        /* Highlight the page you're on */
        .st-key-nav_{current} [data-testid="stPageLink"] a {{
            background: #FA4616 !important;
            border-color: #FA4616 !important;
        }}
        .st-key-nav_{current} [data-testid="stPageLink"] a p {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.container(key="navbar"):
        cols = st.columns([3, 1, 1, 1, 3])
        for col, (label, path, icon) in zip(cols[1:4], pages):
            with col:
                with st.container(key=f"nav_{label}"):
                    st.page_link(path, label=label, icon=icon, use_container_width=True)


def get_recommendations(query: str, spots: list) -> list:
    # Placeholder: simple keyword match on tags and names.
    # Replace with your real filtering / LLM logic.
    words = query.lower().split()
    matches = [
        s for s in spots
        if any(w in " ".join(s["tags"]).lower() or w in s["name"].lower() for w in words)
    ]
    return matches[:5] or spots[:5]