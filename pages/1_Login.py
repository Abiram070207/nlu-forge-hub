import streamlit as st
import json, os

st.set_page_config(page_title="Login", layout="centered")
st.title("🔐 Login / Register")

users_file = "data/users.json"
if not os.path.exists(users_file):
    os.makedirs("data", exist_ok=True)
    with open(users_file, "w") as f:
        json.dump({}, f)

with open(users_file, "r") as f:
    users = json.load(f)

option = st.radio("Choose", ["Login","Register"])
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if option == "Register":
    if st.button("Create Account"):
        if not username or not password:
            st.error("Enter username and password")
        elif username in users:
            st.error("User exists")
        else:
            users[username] = {"password": password}
            with open(users_file, "w") as f:
                json.dump(users, f, indent=2)
            st.success("Account created. Please login.")

else:
    if st.button("Login"):
        if username in users and users[username]['password'] == password:
            st.session_state['user'] = username
            st.success(f"Welcome {username}! You can go to Workspaces page.")
        else:
            st.error("Invalid credentials")
