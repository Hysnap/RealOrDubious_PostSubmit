import os
import gc
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import spacy

# Load SpaCy model once
nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
STOP_WORDS = nlp.Defaults.stop_words


def preprocess_text_for_unigrams(text):
    """Lemmatizes and removes stopwords from a given text string for unigram analysis."""
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)


def safe_stats(series):
    values = series[series > 0].to_numpy()
    if len(values) == 0:
        return 0, 0.0, 0.0
    if len(values) == 1:
        return values[0], float(values[0]), 0.0
    return values.max(), values.mean(), values.std(ddof=0)


def process_ngram(df, n, vocab_filter, text_column, label_column,
                  output_csv, min_count_threshold, write_header, progress_fn):
    """Processes a single n-gram level and appends the result to CSV."""
    progress_fn(f"🔍 Processing {n}-grams...")

    if n == 1:
        df["__cleaned"] = df[text_column].apply(preprocess_text_for_unigrams)
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(df["__cleaned"])
    else:
        vectorizer = CountVectorizer(ngram_range=(n, n), stop_words=None)
        X = vectorizer.fit_transform(df[text_column])

    terms = vectorizer.get_feature_names_out()
    term_matrix = pd.DataFrame.sparse.from_spmatrix(X, columns=terms)

    is_real = df[label_column] == 1
    is_dubious = df[label_column] == 0

    summary_rows = []

    for term in terms:
        col = term_matrix[term]
        real_counts = col[is_real]
        dubious_counts = col[is_dubious]

        count_real = real_counts.sum()
        count_dubious = dubious_counts.sum()
        total_count = count_real + count_dubious

        if total_count < min_count_threshold:
            continue

        if n > 1 and not any(base in vocab_filter for base in term.split()):
            continue

        if n == 1:
            vocab_filter.add(term)

        max_r, mean_r, std_r = safe_stats(real_counts)
        max_d, mean_d, std_d = safe_stats(dubious_counts)

        row = {
            "term": term,
            "ngram_size": n,
            "is_phrase": n > 1,

            "count_real": int(count_real),
            "count_dubious": int(count_dubious),
            "total_count": int(total_count),

            "in_real": count_real > 0,
            "in_dubious": count_dubious > 0,

            "max_real": int(max_r),
            "mean_real": round(mean_r, 4),
            "stdev_real": round(std_r, 4),

            "max_dubious": int(max_d),
            "mean_dubious": round(mean_d, 4),
            "stdev_dubious": round(std_d, 4),
        }

        try:
            row["relevance_score"] = abs(count_real - count_dubious) / total_count
        except ZeroDivisionError:
            row["relevance_score"] = 0.0

        summary_rows.append(row)

    if summary_rows:
        summary_df = pd.DataFrame(summary_rows)
        summary_df.to_csv(output_csv, mode='a', index=False, header=write_header)
        progress_fn(f"✅ Appended {len(summary_rows)} {n}-grams to {output_csv}")
    else:
        progress_fn(f"⚠️ No {n}-grams met the threshold.")


def generate_ngram_summary_csv(
    df, text_column="text", label_column="label",
    output_csv="sl_data_for_dashboard/ngram_summary.csv",
    ngram_range=(1, 3), progress_fn=print,
    min_count_threshold=100):

    df[text_column] = df[text_column].astype(str).fillna("")
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    # Reset output file
    if os.path.exists(output_csv):
        os.remove(output_csv)

    vocab_filter = set()
    write_header = True  # Only write header once

    for n in range(ngram_range[0], ngram_range[1] + 1):
        process_ngram(df, n, vocab_filter, text_column, label_column,
                      output_csv, min_count_threshold, write_header, progress_fn)
        write_header = False
        gc.collect()  # Free memory

    progress_fn(f"📁 All n-grams saved to {output_csv}")


if __name__ == "__main__":
    df = pd.read_csv("sl_data_for_dashboard/preprocessed_wordcloud.zip")
    generate_ngram_summary_csv(
        df,
        output_csv="sl_data_for_dashboard/ngram_summary.csv",
        min_count_threshold=100
    )

# end of ngam_summary_generation.py
#PATH: sl_components/ngam_summary_generation.py