import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import joblib
import json
import os

# -------- CONFIG --------
MODEL_TYPE = "classification"  # or "classification"
DATA_DIR = "ML_model2_models"
MODEL_PATH = f"{DATA_DIR}/ML_model_{MODEL_TYPE}.pkl"
VECTORIZER_PATH = f"{DATA_DIR}/vectorizer_{MODEL_TYPE}.pkl"
SUMMARY_PATH = f"{DATA_DIR}/evaluation_summary.csv"
REPORT_PATH = f"{DATA_DIR}/classification_report.json"
EXPLANATION_PATH = f"{DATA_DIR}/evaluation_explanation.txt"

# -------- Loaders --------
@st.cache_resource
def load_model_and_vectorizer():
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer


def load_summary_metrics():
    return pd.read_csv(SUMMARY_PATH) if os.path.exists(SUMMARY_PATH) else None


def load_classification_report():
    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, "r") as f:
            return json.load(f)
    return None


def load_explanation():
    if os.path.exists(EXPLANATION_PATH):
        with open(EXPLANATION_PATH, "r") as f:
            return f.read()
    return "Explanation not available."


# -------- Main Entry Point --------
def run():
    st.subheader("📰 Fake News Detection Model Dashboard")
    model, vectorizer = load_model_and_vectorizer()

    option = st.sidebar.radio("Choose an option", ["Model Overview", "Test a News Article"])

    if option == "Model Overview":
        st.header("Model Overview")
        st.write(f"### Model Type: RandomForest ({MODEL_TYPE.title()})")

        if hasattr(model, "feature_importances_"):
            st.write("### Feature Importance")
            st.bar_chart(pd.Series(model.feature_importances_, name="Feature Importance"))

        summary_df = load_summary_metrics()
        if summary_df is not None:
            st.write("### Evaluation Summary")
            st.dataframe(summary_df)

        if MODEL_TYPE == "classification":
            # Full classification report
            full_report = load_classification_report()
            if full_report:
                st.write("### Detailed Classification Report")
                st.json(full_report)

            # 🔥 NEW: Load and display confusion matrix heatmap
            conf_path = f"{DATA_DIR}/confusion_matrix.csv"
            if os.path.exists(conf_path):
                st.write("### Confusion Matrix")
                conf_df = pd.read_csv(conf_path)

                # Reshape into matrix
                matrix = [
                    [conf_df["True Negatives"][0], conf_df["False Positives"][0]],
                    [conf_df["False Negatives"][0], conf_df["True Positives"][0]]
                ]

                fig, ax = plt.subplots()
                sns.heatmap(matrix,
                            annot=True,
                            fmt="d",
                            cmap="Blues",
                            xticklabels=["Predicted Fake", "Predicted Real"],
                            yticklabels=["Actual Fake", "Actual Real"],
                            ax=ax)
                st.pyplot(fig)

        st.write("### Evaluation Metrics Explanation")
        st.markdown(load_explanation())

    elif option == "Test a News Article":
        st.header("Test a News Article")
        uploaded_file = st.file_uploader("Upload a `.txt` file with the news article", type=["txt"])

        if uploaded_file:
            text = uploaded_file.read().decode("utf-8")
            st.write("### Preview of Uploaded Text")
            st.text(text[:500] + "..." if len(text) > 500 else text)

            X_input = vectorizer.transform([text])
            prediction = model.predict(X_input)[0]

            st.write("### Prediction Result")

            if MODEL_TYPE == "classification":
                realness_score = model.predict_proba(X_input)[0][1]
                if prediction == 1:
                    st.success(f"🟢 Real News — Confidence: `{realness_score:.2f}`")
                else:
                    st.error(f"🔴 Fake News — Confidence: `{1 - realness_score:.2f}`")
            else:
                st.info(f"Predicted Realness Score: `{prediction:.2f}` (range: 1 = Fake, 5 = Real)")
