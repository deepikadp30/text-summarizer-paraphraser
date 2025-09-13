from transformers import pipeline

# Load summarizer model
def get_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

