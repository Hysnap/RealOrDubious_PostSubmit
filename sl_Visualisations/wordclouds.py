import os
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def generate_wordcloud_from_summary(df, filename, ngram_size=None, filter_fn=None,
                                    output_dir="wordclouds", progress_fn=print):
    """
    Generate a word cloud from the ngram summary DataFrame.
    """
    os.makedirs(output_dir, exist_ok=True)

    subset = df.copy()
    if ngram_size:
        subset = subset[subset["ngram_size"] == ngram_size]
    if filter_fn:
        subset = subset[filter_fn(subset)]

    # Build text for WordCloud
    text = " ".join([
        (row["term"] + " ") * (row["count_real"] + row["count_dubious"])
        for _, row in subset.iterrows()
    ])

    if not text.strip():
        progress_fn(f"⚠️ No terms found for: {filename}")
        return

    wc = WordCloud(width=800, height=400, background_color="white").generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    plt.tight_layout()

    path = os.path.join(output_dir, filename)
    fig.savefig(path)
    plt.close(fig)
    progress_fn(f"🎨 Saved: {path}")

# # === Example usage ===
# if __name__ == "__main__":
#     csv_path = "sl_data_for_dashboard/preprocessed_wordcloud.zip"
#     df = pd.read_csv(csv_path)
#     generate_wordcloud_images(df)