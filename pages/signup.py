import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.db_connection import create_user

st.title("📝 Sign Up Page")

with st.form("signup_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    submitted = st.form_submit_button("Create Account")

    if submitted:
        if name and email and username and password:
            success = create_user(name, email, username, password)
            if success:
                st.success("✅ Account created successfully! Redirecting to login...")
                st.switch_page("pages/login.py")  # ✅ redirect to login page
            else:
                st.error("❌ Failed to create account (maybe username/email exists)")
        else:
            st.warning("⚠️ Please fill in all fields")
