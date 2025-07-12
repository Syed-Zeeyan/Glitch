#signup
import streamlit as st
from utils.auth import signup_user

def show_signup():
    if st.session_state.get("logged_in"):
        st.session_state["page"] = "home"
        st.stop()

    # --- Dark Mode CSS ---
    st.markdown("""
        <style>
        /* Remove default Streamlit padding */
        .block-container {
            padding: 0rem !important;
            margin: 0 auto !important;
            background-color: transparent !important;
            box-shadow: none !important;
    }

        /* Body and app background */
        html, body, .stApp {
            background-color: #0d0d0d !important;
            margin: 0 !important;
            padding: 0 !important;
    }

        /* Signup card style */
        .signup-card {
            background-color: #1e1e1e;
            padding: 3rem 2rem 2rem 2rem;
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
            max-width: 400px;
            margin: 8vh auto;
        }

        .signup-title {
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

    # --- Signup Card UI ---
    st.markdown('<div class="signup-card">', unsafe_allow_html=True)
    st.markdown('<div class="signup-title">📝 Signup for DeFi Credit Agent</div>', unsafe_allow_html=True)

    name = st.text_input("👤 Full Name", placeholder="Enter your full name")
    age = st.number_input("🎂 Age", min_value=18, max_value=100)
    email = st.text_input("📧 Email", placeholder="Enter your email")
    password = st.text_input("🔑 Password", type="password", placeholder="Enter a strong password")

    if st.button("Signup", use_container_width=True):
        success, msg = signup_user(name, age, email, password)
        if success:
            st.success(msg)
            st.session_state["page"] = "login"
            st.stop()
        else:
            st.error(msg)

    st.markdown("---")

    if st.button("🔙 Back to Login", use_container_width=True):
        st.session_state["page"] = "login"
        st.stop()

    st.markdown('</div>', unsafe_allow_html=True)
