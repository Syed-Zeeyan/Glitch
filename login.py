#login

import streamlit as st
from utils.auth import login_user

def show_login():
    if st.session_state.get("logged_in"):
        st.session_state["page"] = "home"
        st.stop()

    # --- CSS: Clean layout & keep dark theme ---
    st.markdown("""
        <style>
        /* Remove default padding/margin */
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
        }

        /* Body dark background */
        body, .stApp {
            background-color: #0d0d0d !important;
            color: white;
        }

        /* Login card styling */
        .login-card {
            background-color: #1e1e1e;
            padding: 3rem 2rem 2rem 2rem;
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
            max-width: 400px;
            margin: 8vh auto;
        }

        .login-title {
            font-size: 1.8rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 2rem;
            color: #eaeaea;
        }

        .footer-text {
            text-align: center;
            margin-top: 2rem;
            font-size: 0.9rem;
            color: #aaaaaa;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Login UI ---
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">🔐 Login to DeFi Credit Agent</div>', unsafe_allow_html=True)

    email = st.text_input("📧 Email", placeholder="Enter your email")
    password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")

    if st.button("Login", use_container_width=True):
        success, msg = login_user(email, password)
        if success:
            st.success(msg)
            st.session_state["logged_in"] = True
            st.session_state["email"] = email
            st.session_state["page"] = "home"
            st.stop()
        else:
            st.error(msg)

    st.markdown("---")

    if st.button("📝 Don’t have an account? Sign up", use_container_width=True):
        st.session_state["page"] = "signup"
        st.stop()

    st.markdown('</div>', unsafe_allow_html=True)
