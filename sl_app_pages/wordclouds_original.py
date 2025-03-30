import streamlit as st
from pathlib import Path
from PIL import Image
import re
import os


def wordcloud_explorer():
    st.title("🧠 WordCloud Explorer")

    # --- Configuration ---
    BASE_DIR = Path.cwd()
    IMAGE_DIR = BASE_DIR / "wordclouds"

    CATEGORY_LABELS = {
        "real": "Real",
        "dubious": "Dubious",
        "all": "Overall",
        "real_unique": "Real (Unique)",
        "dubious_unique": "Dubious (Unique)",
        "common": "Common to Both"
    }

    PHRASE_LABELS = {
        1: "Single Words",
        2: "2-word Phrases",
        3: "3-word Phrases"
    }

    # --- Load image metadata ---
    pattern = re.compile(r"wordcloud_(\w+)_([123])gram_(\d{4})\.png")
    cloud_data = []

    for path in IMAGE_DIR.glob("*.png"):
        match = pattern.match(path.name)
        if match:
            category, ngram, year = match.groups()
            cloud_data.append({
                "path": path,
                "category": category,
                "ngram": int(ngram),
                "year": int(year)
            })

    if not cloud_data:
        st.error("❌ No word cloud images found in the 'wordclouds/' folder.")
        return

    # --- Sidebar filters ---
    all_years = sorted({d["year"] for d in cloud_data})
    all_ngrams = sorted({d["ngram"] for d in cloud_data})

    with st.sidebar:
        st.header("🔧 Filters")
        selected_ngram = st.selectbox(
            "Word/Phrase Type",
            all_ngrams,
            format_func=lambda n: PHRASE_LABELS.get(n, f"{n}-word")
        )
        selected_years = st.multiselect("Select Years to Compare",
                                        all_years, default=all_years)

    st.markdown(f"### Displaying: {PHRASE_LABELS[selected_ngram]}")

    # --- Primary comparison view (Real, Dubious, Overall) ---
    for year in selected_years:
        st.markdown(f"## 📅 Year: {year}")
        cols = st.columns(3)

        for idx, category_key in enumerate(["real", "dubious", "all"]):
            match = next(
                (d for d in cloud_data if d["year"] == year and d["ngram"] == selected_ngram and d["category"] == category_key),
                None
            )
            with cols[idx]:
                st.markdown(f"**{CATEGORY_LABELS.get(category_key, category_key)}**")
                if match:
                    img_path = match["path"]
                    try:
                        img = Image.open(img_path)
                        st.image(img, use_container_width=True)
                    except Exception as e:
                        st.error(f"❌ Failed to open image: {match['path'].name}")
                        st.exception(e)
                else:
                    st.warning("Not found")

    # --- Unique and shared comparisons ---
    st.markdown("---")
    st.subheader("🔍 Unique and Shared Word Clouds")

    for year in selected_years:
        st.markdown(f"### Year: {year}")
        cols = st.columns(3)

        for idx, category_key in enumerate(["real_unique",
                                            "dubious_unique",
                                            "common"]):
            match = next(
                (d for d in cloud_data if d["year"] == year and d["ngram"] == selected_ngram and d["category"] == category_key),
                None
            )
            with cols[idx]:
                st.markdown(f"**{CATEGORY_LABELS.get(category_key, category_key)}**")
                if match:
                    img_path = match["path"]
                    try:
                        img = Image.open(img_path)
                        st.image(img, use_container_width=True)
                    except Exception as e:
                        st.error(f"❌ Failed to open image: {match['path'].name}")
                        st.exception(e)
                else:
                    st.warning("Not found")

    st.caption("Images are displayed from local 'wordclouds' directory."
               " Click to zoom or right-click to open in a new tab.")
