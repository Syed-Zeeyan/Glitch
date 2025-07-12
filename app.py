# app.py
import streamlit as st
from login import show_login
from signup import show_signup
from home import show_home

st.set_page_config(
    page_title="DeFi Credit Agent",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "page" not in st.session_state:
    st.session_state["page"] = "login"

# Route manually
if st.session_state["page"] == "login":
    show_login()
elif st.session_state["page"] == "signup":
    show_signup()
elif st.session_state["page"] == "home":
    show_home()
