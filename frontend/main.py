import streamlit as st
import requests

placeholder = st.empty()

with placeholder.form("login"):
    st.markdown("#### Enter your credentials")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit and username == "" and password == "":
    st.warning("Please fill in the form.")
elif submit and username == "":
    st.warning("Please fill in your email.")
elif submit and password == "":
    st.warning("Please fill in your password.")

if submit and username != "" and password != "":
    response = requests.post('http://localhost:8000/api/v1/signin', data={"username": username, "password": password})
    if response.status_code == 200:
        st.success("Login successful")
    else:
        st.error("Login failed")