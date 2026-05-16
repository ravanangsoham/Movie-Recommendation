import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import random

st.set_page_config(
    page_title="CineScope India Pro",
    page_icon="🎬",
    layout="wide"
)

FILE = "soham.txt"

if not os.path.exists(FILE):
    st.error("❌ soham.txt file not found")
    st.stop()

data = pd.read_csv(
    FILE,
    names=["Movie", "Genre", "Rating", "OTT"]
)

data["Rating"] = pd.to_numeric(data["Rating"], errors="coerce")
data = data.dropna()

st.title("🎬 CineScope India Pro")

st.markdown("## Smart Movie Recommendation System")

st.sidebar.title("Filters")

search = st.sidebar.text_input("Search Movie")

genre = st.sidebar.selectbox(
    "Genre",
    ["All"] + sorted(data["Genre"].unique())
)

ott = st.sidebar.selectbox(
    "OTT Platform",
    ["All"] + sorted(data["OTT"].unique())
)

filtered = data.copy()

if genre != "All":
    filtered = filtered[filtered["Genre"] == genre]

if ott != "All":
    filtered = filtered[filtered["OTT"] == ott]

if search:
    filtered = filtered[
        filtered["Movie"].str.lower().str.contains(search.lower())
    ]

col1, col2, col3 = st.columns(3)

col1.metric("Movies", len(filtered))

col2.metric(
    "Average Rating",
    round(filtered["Rating"].mean(), 1)
)

col3.metric(
    "Platforms",
    filtered["OTT"].nunique()
)

st.subheader("Movie Dataset")

st.dataframe(filtered, use_container_width=True)

# TOP MOVIES

st.subheader("🏆 Top Rated Movies")

top = filtered.sort_values(
    by="Rating",
    ascending=False
).head(10)

fig, ax = plt.subplots(figsize=(10,5))

colors = plt.cm.plasma(
    [i/len(top) for i in range(len(top))]
)

bars = ax.bar(
    top["Movie"],
    top["Rating"],
    color=colors
)

for bar in bars:

    h = bar.get_height()

    ax.text(
        bar.get_x()+bar.get_width()/2,
        h+0.1,
        str(round(h,1)),
        ha='center'
    )

plt.xticks(rotation=20)

ax.set_title("Top Rated Movies")

st.pyplot(fig)

# GENRE GRAPH

st.subheader("🎭 Genre Distribution")

genre_count = filtered["Genre"].value_counts()

fig2, ax2 = plt.subplots(figsize=(10,5))

bars = ax2.bar(
    genre_count.index,
    genre_count.values,
    color=plt.cm.Set3(range(len(genre_count)))
)

for bar in bars:

    h = bar.get_height()

    ax2.text(
        bar.get_x()+bar.get_width()/2,
        h+0.2,
        str(h),
        ha='center'
    )

plt.xticks(rotation=20)

ax2.set_title("Genre Analytics")

st.pyplot(fig2)

# OTT PIE CHART

st.subheader("📡 OTT Analysis")

ott_count = filtered["OTT"].value_counts()

fig3, ax3 = plt.subplots(figsize=(7,7))

ax3.pie(
    ott_count.values,
    labels=ott_count.index,
    autopct='%1.1f%%',
    shadow=True
)

st.pyplot(fig3)

# TRENDING

st.subheader("🔥 Trending Movies")

if len(filtered) >= 5:
    trending = filtered.sample(5)
else:
    trending = filtered

fig4, ax4 = plt.subplots(figsize=(10,5))

bars = ax4.barh(
    trending["Movie"],
    trending["Rating"],
    color=plt.cm.viridis(
        [i/len(trending) for i in range(len(trending))]
    )
)

st.pyplot(fig4)

# RANDOM MOVIE

st.subheader("🎲 Random Recommendation")

if st.button("Suggest Movie"):

    movie = filtered.sample(1).iloc[0]

    st.success(
        f"{movie['Movie']} | ⭐ {movie['Rating']} | 📡 {movie['OTT']}"
    )
