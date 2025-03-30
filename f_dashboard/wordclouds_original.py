import streamlit as st
from pathlib import Path
from PIL import Image
import re


def wordcloud_explorer():
    st.title("🧠 WordCloud Explorer (All Years)")

    # --- Configuration ---
    IMAGE_DIR = Path("wordclouds")  # This should be at the root of your app
    CATEGORY_LABELS = {
        "real": "Real",
        "dubious": "Dubious",
        "all": "Overall"
    }
    PHRASE_LABELS = {
        1: "Single Words",
        2: "2-word Phrases",
        3: "3-word Phrases"
    }
    VALID_CATEGORIES = set(CATEGORY_LABELS.keys())

    # --- Parse available files ---
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
        st.error("❌ No word cloud images found in 'wordclouds/'")
        return

    # --- Sidebar controls ---
    all_years = sorted({d["year"] for d in cloud_data})
    available_ngrams = sorted({d["ngram"] for d in cloud_data if d["category"] in VALID_CATEGORIES})

    with st.sidebar:
        st.header("🔧 Controls")
        selected_ngram = st.selectbox(
            "Word/Phrase Type",
            available_ngrams,
            format_func=lambda n: PHRASE_LABELS.get(n, f"{n}-word"),
            key="wordcloud_phrase_selector"
        )
        # word_limit = st.slider("Max Words (visual density only)", 10, 200, 100)

    st.markdown(f"### Displaying: {PHRASE_LABELS[selected_ngram]} — Top Words")

    # --- Display word clouds grouped by year ---
    for year in all_years:
        st.markdown(f"## 📅 Year: {year}")
        cols = st.columns(3)

        for idx, category_key in enumerate(["real", "dubious", "all"]):
            match = next(
                (d for d in cloud_data
                 if d["ngram"] == selected_ngram and
                    d["year"] == year and
                    d["category"] == category_key),
                None
            )

            with cols[idx]:
                st.markdown(f"**{CATEGORY_LABELS[category_key]}**")
                if match:
                    img_path = match["path"]
                    public_url = f"/wordclouds/{img_path.name}"

                    # Clickable image that links to fullscreen version
                    st.markdown(
                        f"""
                        <a href="{public_url}" target="_blank">
                            <img src="{public_url}" style="width: 100%; border-radius: 4px; margin-bottom: 6px;" />
                        </a>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.warning("Not found")
