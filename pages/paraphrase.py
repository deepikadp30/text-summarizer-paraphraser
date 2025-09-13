import streamlit as st
from transformers import pipeline
import textstat
import plotly.express as px

# -----------------------------
# Load Paraphraser
# -----------------------------
@st.cache_resource
def load_paraphraser():
    return pipeline("text2text-generation", model="Vamsi/T5_Paraphrase_Paws")

paraphraser = load_paraphraser()

# -----------------------------
# Function to calculate readability
# -----------------------------
def calculate_readability(text):
    return {
        "Flesch Reading Ease": textstat.flesch_reading_ease(text),
        "Gunning Fog": textstat.gunning_fog(text),
        "SMOG Index": textstat.smog_index(text),
        "Automated Readability Index": textstat.automated_readability_index(text),
        "Dale-Chall": textstat.dale_chall_readability_score(text),
    }

# -----------------------------
# Streamlit UI
# -----------------------------
def main():
    st.title("📝 Paraphrasing Tool with Readability Comparison")

    st.markdown("Upload a text file or type text below to get a paraphrased version.")

    # File Upload
    uploaded_file = st.file_uploader("📂 Upload a text file", type=["txt"])
    input_text = ""

    if uploaded_file is not None:
        input_text = uploaded_file.read().decode("utf-8")
        st.text_area("📖 Extracted Text", input_text, height=200)

    # Text Area
    user_text = st.text_area("✍️ Or type/paste your text here:", value=input_text, height=200)

    # Difficulty Level
    level = st.radio("⚡ Choose Paraphrasing Level", ["Beginner", "Intermediate", "Advanced"])

    # Paraphrasing Style
    style = st.selectbox(
        "🎨 Choose Paraphrasing Style",
        ["Fluency", "Formal", "Creative", "Concise"]
    )

    if st.button("Paraphrase"):
        if user_text.strip():
            # Adjust paraphrasing based on level
            if level == "Beginner":
                num_return = 1
                max_len = 100
            elif level == "Intermediate":
                num_return = 2
                max_len = 150
            else:  # Advanced
                num_return = 3
                max_len = 200

            # Add style influence
            style_prompt = f"Paraphrase in a {style.lower()} style: {user_text}"

            # Generate paraphrased versions
            result = paraphraser(
                style_prompt,
                max_length=max_len,
                num_return_sequences=num_return,
                do_sample=True,
                temperature=1.5
            )

            # Take the first paraphrased text for comparison
            paraphrased_text = result[0]['generated_text']

            # Show side-by-side
            st.subheader("📖 Original vs Paraphrased")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original Text**")
                st.write(user_text)
            with col2:
                st.markdown(f"**Paraphrased Versions ({style} Style)**")
                for i, r in enumerate(result):
                    st.write(f"👉 {r['generated_text']}")

            # -----------------------------
            # Readability Comparison
            # -----------------------------
            st.subheader("📊 Readability Scores Comparison")

            original_scores = calculate_readability(user_text)
            paraphrased_scores = calculate_readability(paraphrased_text)

            # Convert to dataframe format for bar chart
            data = []
            for metric in original_scores.keys():
                data.append({"Metric": metric, "Text": "Original", "Score": original_scores[metric]})
                data.append({"Metric": metric, "Text": "Paraphrased", "Score": paraphrased_scores[metric]})

            fig = px.bar(
                data, x="Metric", y="Score", color="Text", barmode="group",
                title=f"Original vs Paraphrased Readability Scores ({style} Style)"
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("⚠️ Please enter or upload some text.")

if __name__ == "__main__":
    main()
