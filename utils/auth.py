# utils/auth.py
import streamlit as st

def get_user_db():
    if "users" not in st.session_state:
        st.session_state["users"] = {}
    return st.session_state["users"]

def signup_user(name, age, email, password):
    users = get_user_db()
    if email in users:
        return False, "User already exists."
    users[email] = {"name": name, "age": age, "password": password}
    return True, "Signup successful."

def login_user(email, password):
    users = get_user_db()
    user = users.get(email)
    if not user:
        return False, "User not found."
    if user["password"] != password:
        return False, "Incorrect password."
    return True, "Login successful."

def get_current_user():
    users = get_user_db()
    email = st.session_state.get("email")
    return users.get(email)
