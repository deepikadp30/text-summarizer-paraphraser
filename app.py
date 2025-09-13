import streamlit as st
from transformers import pipeline

# -----------------------------
# Summarizer model
# -----------------------------
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

summarizer = load_summarizer()

# -----------------------------
# Functions
# -----------------------------
def signup():
    st.title("📝 Signup Page")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")

    if st.button("Signup"):
        if username and password:
            if "users" not in st.session_state:
                st.session_state["users"] = {}
            if username in st.session_state["users"]:
                st.error("⚠️ Username already exists. Please choose another.")
            else:
                st.session_state["users"][username] = password
                st.success("✅ Account created! Please log in now.")
                st.session_state.page = "login"
                st.rerun()
        else:
            st.error("⚠️ Please enter both username and password.")

def login():
    st.title("🔒 Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if "users" in st.session_state and username in st.session_state["users"]:
            if st.session_state["users"][username] == password:
                st.session_state.logged_in = True
                st.success("✅ Login successful! Redirecting...")
                st.session_state.page = "summarizer"
                st.rerun()
            else:
                st.error("❌ Invalid password")
        else:
            st.error("❌ Invalid username or password")

    if st.button("Go to Signup"):
        st.session_state.page = "signup"
        st.rerun()

def summarizer_page():
    st.title("📄 Text Summarizer")

    text = st.text_area("Enter the text you want to summarize:", height=200)

    if st.button("Summarize"):
        if text.strip():
            summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
            st.subheader("✨ Summary:")
            st.write(summary[0]['summary_text'])
        else:
            st.error("⚠️ Please enter some text to summarize.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

# -----------------------------
# Main App
# -----------------------------
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if st.session_state.page == "signup":
        signup()
    elif st.session_state.page == "login":
        login()
    elif st.session_state.page == "summarizer" and st.session_state.logged_in:
        summarizer_page()
    else:
        st.session_state.page = "login"
        login()

if __name__ == "__main__":
    main()
