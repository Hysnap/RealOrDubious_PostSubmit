import streamlit as st
from pathlib import Path
from PIL import Image
import re


def wordcloud_explorer():
    st.title("🧠 WordCloud Explorer")

# === Config ===
    IMAGE_DIR = Path("wordclouds")
    REQUIRED_CATEGORIES = {
    "Real": "real",
    "Dubious": "dubious",
    "Overall": "all"
}
    UNIQUE_CATEGORIES = {
    "Real (Unique)": "real_unique",
    "Dubious (Unique)": "dubious_unique",
    "Common to Both": "common"
}
    PATTERN = re.compile(r"wordcloud_(\w+)_([123])gram_(\d{4})\.png")

# === Load all available images ===
    cloud_data = []
    for path in IMAGE_DIR.glob("*.png"):
        match = PATTERN.match(path.name)
        if match:
            category, ngram, year = match.groups()
            cloud_data.append({
            "path": path,
            "category": category,
            "ngram": int(ngram),
            "year": int(year)
        })

    if not cloud_data:
        st.warning("No wordclouds found in the 'wordclouds/' folder.")
        st.stop()

# === Extract dropdown options ===
    years = sorted({d["year"] for d in cloud_data})
    ngrams = sorted({d["ngram"] for d in cloud_data})

    with st.sidebar:
        st.header("🧩 Filters")
        selected_ngram = st.selectbox("Select N-gram Size", ngrams)
        selected_year = st.selectbox("Select Year", years)

    def find_image(category_key):
        for entry in cloud_data:
            if (entry["category"] == category_key and
            entry["ngram"] == selected_ngram and
            entry["year"] == selected_year):
                return entry["path"]
        return None

    def display_columns_from_dict(title_dict):
        cols = st.columns(len(title_dict))
        for col, (label, cat_key) in zip(cols, title_dict.items()):
            with col:
                st.markdown(f"### {label}")
                img_path = find_image(cat_key)
                if img_path:
                    st.image(Image.open(img_path), use_column_width=True)
                else:
                    st.warning("Not found")

# === Tabs Interface ===
    tab1, tab2, tab3 = st.tabs(["🔍 Main Comparison", "🧩 Unique & Common", "🧪 Other Wordclouds"])

    with tab1:
        st.subheader(f"{selected_ngram}-gram | {selected_year}")
        display_columns_from_dict(REQUIRED_CATEGORIES)

    with tab2:
        st.subheader(f"Unique/Common Terms — {selected_ngram}-gram | {selected_year}")
        display_columns_from_dict(UNIQUE_CATEGORIES)

    with tab3:
        st.subheader(f"Other Wordclouds — {selected_ngram}-gram | {selected_year}")
        known_keys = set(REQUIRED_CATEGORIES.values()) | set(UNIQUE_CATEGORIES.values())

        other_imgs = [
        d for d in cloud_data
        if d["ngram"] == selected_ngram and
           d["year"] == selected_year and
           d["category"] not in known_keys
    ]

        if not other_imgs:
            st.info("No additional wordclouds found for this selection.")
        else:
            for item in other_imgs:
                label = item["category"].replace("_", " ").title()
                st.markdown(f"#### {label}")
                st.image(Image.open(item["path"]), use_column_width=True)

return wordcloud_explorer()
