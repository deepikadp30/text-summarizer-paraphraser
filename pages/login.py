import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db_connection import validate_user

st.title("🔒 Login Page")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user = validate_user(username, password)
    if user:
        st.session_state.logged_in = True
        st.session_state.username = user["username"]
        st.success("✅ Login successful! Redirecting to dashboard...")
        st.switch_page("pages/dashboard.py")  # redirect to dashboard
    else:
        st.error("❌ Invalid username or password")

st.page_link("pages/signup.py", label="📝 Create a new account")
