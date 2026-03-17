import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import load_raw_data
from src.data_cleaning import clean_data
from src.analysis import compute_avg_cost_per_country, compute_affordability_index
from src.clustering import apply_kmeans

# Page config
st.set_page_config(
    page_title="Global Cost of Living",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cacher la navigation automatique de Streamlit
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Load & cache data
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, 'data', 'raw', 'cost-of-living.csv')
    df = load_raw_data(raw_path)
    df = clean_data(df)
    df = compute_avg_cost_per_country(df)
    df = compute_affordability_index(df)
    df = apply_kmeans(df, n_clusters=3)
    return df

df = load_data()

# Sidebar navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/44/44386.png", width=60)
st.sidebar.title("🌍 Cost of Living")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["🌐 World Overview", "🏙️ Country & City Explorer", "🤖 Clustering Analysis"]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "📊 Data source: [Numbeo via Kaggle](https://www.kaggle.com/datasets/mvieira101/global-cost-of-living)"
)
st.sidebar.markdown(f"🏙️ **{len(df)}** cities | 🌍 **{df['country'].nunique()}** countries")

#  Route pages
if page == "🌐 World Overview":
    from app.pages.overview import show
    show(df)
elif page == "🏙️ Country & City Explorer":
    from app.pages.country_view import show
    show(df)
elif page == "🤖 Clustering Analysis":
    from app.pages.clustering_view import show
    show(df)