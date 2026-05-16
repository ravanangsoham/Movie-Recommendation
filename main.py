import streamlit as st
import pandas as pd
import os
import random
import numpy as np

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="CineScope India Pro",
    page_icon="🎬",
    layout="wide"
)

# ============================================
# FILE
# ============================================

FILE = "soham.txt"

# ============================================
# LOAD DATA
# ============================================

if not os.path.exists(FILE):
    st.error("❌ soham.txt file not found")
    st.stop()

try:
    data = pd.read_csv(
        FILE,
        names=["Movie", "Genre", "Rating", "OTT"]
    )

except Exception as e:
    st.error(f"❌ Dataset Error: {e}")
    st.stop()

# ============================================
# CLEAN DATA
# ============================================

data["Movie"] = data["Movie"].astype(str)
data["Genre"] = data["Genre"].astype(str)
data["OTT"] = data["OTT"].astype(str)

data["Rating"] = pd.to_numeric(
    data["Rating"],
    errors="coerce"
)

data = data.dropna()

# ============================================
# CSS DESIGN
# ============================================

st.markdown("""
<style>

.main {
    background-color: #d8f3dc;
}

section[data-testid="stSidebar"] {
    background-color: #95d5b2;
}

h1,h2,h3 {
    color: #1b4332;
}

[data-testid="metric-container"] {
    background-color: white;
    border-radius: 12px;
    padding: 15px;
}

.stButton>button {
    background-color: #2d6a4f;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# TITLE
# ============================================

st.title("🎬 CineScope India Pro")

st.markdown(
    "### Smart Movie Recommendation & OTT Analytics Dashboard"
)

# ============================================
# SIDEBAR
# ============================================

st.sidebar.title("⚙ Filters")

search = st.sidebar.text_input("🔍 Search Movie")

genre = st.sidebar.selectbox(
    "🎭 Genre",
    ["All"] + sorted(data["Genre"].unique())
)

ott = st.sidebar.selectbox(
    "📡 OTT Platform",
    ["All"] + sorted(data["OTT"].unique())
)

min_rating = st.sidebar.slider(
    "⭐ Minimum Rating",
    0.0,
    10.0,
    5.0
)

# ============================================
# FILTER DATA
# ============================================

filtered = data.copy()

if genre != "All":
    filtered = filtered[
        filtered["Genre"] == genre
    ]

if ott != "All":
    filtered = filtered[
        filtered["OTT"] == ott
    ]

filtered = filtered[
    filtered["Rating"] >= min_rating
]

if search:
    filtered = filtered[
        filtered["Movie"].str.lower().str.contains(
            search.lower(),
            na=False
        )
    ]

# ============================================
# METRICS
# ============================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🎬 Movies",
        len(filtered)
    )

with col2:
    st.metric(
        "⭐ Average Rating",
        round(filtered["Rating"].mean(), 1)
        if len(filtered) > 0 else 0
    )

with col3:
    st.metric(
        "📡 Platforms",
        filtered["OTT"].nunique()
    )

# ============================================
# DATA TABLE
# ============================================

st.subheader("📋 Movie Dataset")

st.dataframe(
    filtered,
    use_container_width=True
)

# ============================================
# TOP MOVIES
# ============================================

st.subheader("🏆 Top Rated Movies")

top_movies = filtered.sort_values(
    by="Rating",
    ascending=False
).head(10)

st.bar_chart(
    top_movies.set_index("Movie")["Rating"]
)

# ============================================
# GENRE ANALYSIS
# ============================================

st.subheader("🎭 Genre Distribution")

genre_count = filtered["Genre"].value_counts()

st.bar_chart(genre_count)

# ============================================
# OTT ANALYSIS
# ============================================

st.subheader("📡 OTT Platform Analysis")

ott_count = filtered["OTT"].value_counts()

st.bar_chart(ott_count)

# ============================================
# TRENDING MOVIES
# ============================================

st.subheader("🔥 Trending Movies")

if len(filtered) >= 5:
    trending = filtered.sample(5)
else:
    trending = filtered

st.dataframe(trending)

# ============================================
# RECOMMENDATIONS
# ============================================

st.subheader("💡 Smart Recommendations")

recommend = filtered.sort_values(
    by="Rating",
    ascending=False
).head(5)

for i, row in recommend.iterrows():

    st.success(
        f"🎬 {row['Movie']} | ⭐ {row['Rating']} | 📡 {row['OTT']}"
    )

# ============================================
# RANDOM MOVIE
# ============================================

st.subheader("🎲 Random Movie Suggestion")

if st.button("Suggest Me a Movie"):

    movie = filtered.sample(1).iloc[0]

    st.info(f"""
🎬 Movie: {movie['Movie']}

🎭 Genre: {movie['Genre']}

⭐ Rating: {movie['Rating']}

📡 OTT: {movie['OTT']}
""")

# ============================================
# FOOTER
# ============================================

st.markdown("---")

st.markdown(
    "## ✅ Developed using Streamlit & Pandas"
)
