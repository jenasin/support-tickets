import streamlit as st
import pandas as pd
import os

# Filepath for storing data
CSV_FILE = "field_data.csv"

# Create or load dataset
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

# User authentication
users = {"user1": "pass", "user2": "pass", "user3": "pass", "user4": "pass", "user5": "pass"}

st.set_page_config(page_title="Farm Data Manager", layout="wide")
st.sidebar.title("🔑 Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

if username in users and users[username] == password:
    st.sidebar.success(f"Welcome, {username}!")
    
    page = st.sidebar.radio("Select a Page", ["View Data", "Edit Data"])
    
    st.title("🌾 Farm Data Manager")
    
    if page == "View Data":
        st.write("### Current Field Data")
        st.dataframe(data, use_container_width=True)
    
    elif page == "Edit Data":
        st.write("### Edit Field Data")
        data = st.data_editor(data, num_rows="dynamic")
        
        if st.button("Save Data"):
            data.to_csv(CSV_FILE, index=False)
            st.success("Data successfully saved!")
else:
    st.sidebar.warning("Invalid username or password. Please try again.")
