import streamlit as st

st.title("📊 Dashboard")

# Check if logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please log in first.")
    st.switch_page("pages/login.py")

st.success(f"Welcome {st.session_state.username} 🎉")

# Example content
st.subheader("Your Dashboard")
st.write("✅ Text Summarizer")
st.write("✅ Paraphrasing Tool")
st.write("✅ User Profile")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.switch_page("app.py")
