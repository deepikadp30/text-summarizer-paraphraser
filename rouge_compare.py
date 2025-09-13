# pages/rouge_compare.py
import streamlit as st
from rouge_score import rouge_scorer
import plotly.express as px

st.title("ROUGE Score Visual Representation")

# Input boxes
original_text = st.text_area("Enter Original Text", height=150)
generated_text = st.text_area("Enter Summarized/Paraphrased Text", height=150)

if st.button("Calculate ROUGE"):
    if original_text.strip() and generated_text.strip():
        # Initialize ROUGE scorer
        scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        scores = scorer.score(original_text, generated_text)

        # Extract precision/recall/f1 (we’ll use f1 score here)
        rouge_scores = {
            "ROUGE-1": scores["rouge1"].fmeasure,
            "ROUGE-2": scores["rouge2"].fmeasure,
            "ROUGE-L": scores["rougeL"].fmeasure,
        }

        # Show scores
        st.write("### ROUGE Scores (F1 Measure)")
        st.json({k: round(v, 3) for k, v in rouge_scores.items()})

        # Plot bar chart
        fig = px.bar(
            x=list(rouge_scores.keys()),
            y=list(rouge_scores.values()),
            labels={'x': 'ROUGE Metric', 'y': 'ROUGE Score'},
            title="ROUGE Visual Representation"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please enter both Original and Generated text.")
