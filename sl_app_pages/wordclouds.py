import streamlit as st
from pathlib import Path
from PIL import Image
import re


def wordcloud_explorer():
    st.title("🧠 WordCloud Explorer (All Years)")

    # --- Configuration ---
    STATIC_DIR = Path("static/wordclouds")  # Where images are now stored
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

    for path in STATIC_DIR.glob("*.png"):
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
        st.error("❌ No word cloud images found in 'static/wordclouds/'")
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
        word_limit = st.slider("Max Words (visual density only)", 10, 200, 100)

    st.markdown(f"### Displaying: {PHRASE_LABELS[selected_ngram]} — Top {word_limit} Words")

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
                    st.image(Image.open(img_path), use_container_width=True)

                    # Public URL for the browser to access
                    public_url = f"/static/wordclouds/{img_path.name}"

                    # Add link to view fullscreen
                    st.markdown(
                        f'<a href="{public_url}" target="_blank">🔍 Click to view fullscreen</a>',
                        unsafe_allow_html=True
                    )
                else:
                    st.warning("Not found")

    st.caption("Note: Word count limit is currently visual-only. Adjust during generation for stricter filtering.")

