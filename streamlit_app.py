import streamlit as st
import pandas as pd
import os

# Filepath for storing data
CSV_FILE = "field_data.csv"
USER_FILE = "users.csv"

# Create or load user dataset
def load_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    else:
        users = pd.DataFrame({
            "Username": ["admin", "editor1", "editor2", "viewer1", "viewer2"],
            "Password": ["pass", "pass", "pass", "pass", "pass"],
            "Role": ["admin", "editor", "editor", "viewer", "viewer"]
        })
        users.to_csv(USER_FILE, index=False)
        return users

def load_data():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        data = pd.DataFrame({
            "Pole": ["Pole A", "Pole B", "Pole C", "Pole D", "Pole E", "Pole F", "Pole G", "Pole H", "Pole I", "Pole J"],
            "Plodina": ["Pšenice", "Ječmen", "Řepka", "Kukuřice", "Slunečnice", "Oves", "Žito", "Brambory", "Soja", "Cukrová řepa"],
            "Předchozí výnosy (t/ha)": ["4.2, 4.5, 4.8, 5.1", "3.1, 3.4, 3.6, 3.9", "2.8, 3.0, 3.3, 3.6", "6.5, 6.7, 7.0, 7.3", "2.2, 2.5, 2.8, 3.0", "3.6, 3.9, 4.1, 4.4", "3.9, 4.2, 4.4, 4.7", "15.0, 15.5, 16.0, 16.5", "2.5, 2.8, 3.1, 3.3", "50.2, 52.1, 54.3, 56.0"],
            "Výměra (ha)": [10.5, 8, 12.2, 15, 7.5, 9.3, 11, 5.8, 6.4, 14.7]
        })
        data.to_csv(CSV_FILE, index=False)
        return data

data = load_data()
users = load_users()

# User authentication
st.set_page_config(page_title="Farm Data Manager", layout="wide")
st.sidebar.title("🔑 Login")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.role = ""

if not st.session_state.authenticated:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("Login"):
        user_row = users[(users["Username"] == username) & (users["Password"] == password)]
        if not user_row.empty:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = user_row.iloc[0]["Role"]
            st.sidebar.success(f"Welcome, {username} ({st.session_state.role})!")
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password. Please try again.")
else:
    st.sidebar.write(f"Logged in as: **{st.session_state.username} ({st.session_state.role})**")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()
    
    page = st.sidebar.radio("Select a Page", ["View Data", "Edit Data" if st.session_state.role in ["admin", "editor"] else "View Only"])
    
    st.title("🌾 Farm Data Manager")
    
    if page == "View Data" or page == "View Only":
        st.write("### Current Field Data")
        st.dataframe(data, use_container_width=True)
    
    elif page == "Edit Data":
        st.write("### Edit Field Data")
        data = st.data_editor(data, num_rows="dynamic")
        
        if st.button("Save Data"):
            data.to_csv(CSV_FILE, index=False)
            st.success("Data successfully saved!")
