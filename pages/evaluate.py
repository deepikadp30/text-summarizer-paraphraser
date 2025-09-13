import streamlit as st
from transformers import pipeline
from rouge_score import rouge_scorer
import textstat
import plotly.express as px

# -----------------------------
# Summarizer Loader (cached)
# -----------------------------
@st.cache_resource
def load_summarizer(model_name):
    return pipeline("summarization", model=model_name)

# -----------------------------
# Calculate ROUGE
# -----------------------------
def calculate_rouge(reference, generated):
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    return scorer.score(reference, generated)

# -----------------------------
# Calculate readability
# -----------------------------
def get_readability_scores(text):
    return {
        "Flesch Reading Ease": textstat.flesch_reading_ease(text),
        "SMOG Index": textstat.smog_index(text),
        "Flesch-Kincaid Grade": textstat.flesch_kincaid_grade(text),
        "Gunning Fog": textstat.gunning_fog(text),
        "Automated Readability": textstat.automated_readability_index(text),
        "Coleman-Liau": textstat.coleman_liau_index(text),
        "Dale-Chall": textstat.dale_chall_readability_score(text),
    }

# -----------------------------
# Streamlit App
# -----------------------------
def main():
    st.title("📊 Text Evaluation")

    st.markdown(
        """
        Upload a text file, choose summary options, and evaluate the generated summary  
        against the original text using **ROUGE scores** and **Readability analysis**.
        """
    )

    uploaded_file = st.file_uploader("📂 Upload a text file", type=["txt"])
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")

        # Choose summary length
        length_choice = st.radio("📏 Choose Summary Length", ["Short", "Medium", "Long"])
        if length_choice == "Short":
            max_len, min_len = 60, 20
        elif length_choice == "Medium":
            max_len, min_len = 120, 40
        else:  # Long
            max_len, min_len = 200, 80

        # Choose model
        model_choice = st.selectbox(
            "🤖 Choose a Summarization Model",
            ["facebook/bart-large-cnn", "t5-small", "sshleifer/distilbart-cnn-12-6"]
        )

        if st.button("Generate & Evaluate"):
            summarizer = load_summarizer(model_choice)
            summary = summarizer(text, max_length=max_len, min_length=min_len, do_sample=False)[0]['summary_text']

            # Show side-by-side comparison
            st.subheader("📖 Original vs Summary")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original Text**")
                st.write(text)
            with col2:
                st.markdown("**Summary**")
                st.write(summary)

            # Readability Scores
            st.subheader("📊 Readability Scores Comparison")
            orig_scores = get_readability_scores(text)
            sum_scores = get_readability_scores(summary)

            # Prepare chart data
            categories = list(orig_scores.keys())
            orig_values = list(orig_scores.values())
            sum_values = list(sum_scores.values())

            fig = px.bar(
                x=categories + categories,
                y=orig_values + sum_values,
                color=["Original"] * len(categories) + ["Summary"] * len(categories),
                barmode="group",
                labels={"x": "Metric", "y": "Score"},
                title="Original vs Summary Readability"
            )
            st.plotly_chart(fig)

            # ROUGE Scores
            st.subheader("📈 ROUGE Evaluation Results")
            rouge_scores = calculate_rouge(text, summary)
            for metric, result in rouge_scores.items():
                st.write(
                    f"**{metric.upper()}** → Precision: {result.precision:.3f}, "
                    f"Recall: {result.recall:.3f}, F1: {result.fmeasure:.3f}"
                )

if __name__ == "__main__":
    main()
