import streamlit as st
import pandas as pd
import os
from mega import Mega

# ✅ Authenticate with MEGA
mega = Mega()
m = mega.login("your_email@example.com", "your_password")  # Replace with your MEGA credentials

# ✅ Set Up Streamlit App
st.set_page_config(page_title="Data Management App - Runaway", layout="wide")


# Authentication
def check_password():
    """Check user password before accessing the app."""
    st.sidebar.title("Login")
    password = st.sidebar.text_input("Enter Password:", type="password")

    if password == "beautifulmind":
        return True
    else:
        st.sidebar.warning("Incorrect password. Please try again.")
        return False


if not check_password():
    st.stop()

# Define category folders
CATEGORY_FOLDERS = {
    "1000": "1000",
    "125": "125",
    "200": "200",
    "gasti": "Gasti"
}

# Ensure main folders exist
for folder in CATEGORY_FOLDERS.values():
    os.makedirs(folder, exist_ok=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Upload", "Archive", "Cloud Backup", "Contact Me"])

# Home Page
if page == "Home":
    st.title("Welcome to the Data Management App")
    st.write("Use the sidebar to navigate.")

# Upload Page
elif page == "Upload":
    st.title("Upload Files")
    st.write("Upload your daily Excel files.")

    uploaded_files = st.file_uploader("Upload Excel files", type=["xlsx"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name.lower()
            st.subheader(f"Processing: {uploaded_file.name}...")

            # Determine category based on filename
            category = None
            for key in CATEGORY_FOLDERS:
                if key in file_name:
                    category = CATEGORY_FOLDERS[key]
                    break

            if category is None:
                st.warning(f"❌ Category not found for file: {uploaded_file.name}. Skipping...")
                continue

            # Save file locally
            save_path = os.path.join(category, uploaded_file.name)
            if os.path.exists(save_path):
                st.error(f"❌ File '{uploaded_file.name}' already exists in {category}! Upload skipped.")
                continue

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"✅ File saved to {category}/")

# Archive Page
elif page == "Archive":
    st.title("Archive")
    st.write("Browse your saved files.")

    for category, folder in CATEGORY_FOLDERS.items():
        st.subheader(f"📂 {category}")

        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

        if files:
            for file in files:
                st.write(f"📄 {file}")
        else:
            st.write("No files in this category.")

# **💾 Cloud Backup (MEGA)**
elif page == "Cloud Backup":
    st.title("Backup Files to MEGA")

    selected_category = st.selectbox("Select Category to Upload", list(CATEGORY_FOLDERS.values()))

    if selected_category:
        files = [f for f in os.listdir(selected_category) if os.path.isfile(os.path.join(selected_category, f))]

        if files:
            selected_file = st.selectbox("Select File to Upload to MEGA", files)

            if selected_file:
                file_path = os.path.join(selected_category, selected_file)

                # ✅ Upload file to MEGA
                m.upload(file_path)

                st.success(f"✅ File '{selected_file}' uploaded to MEGA cloud storage!")
        else:
            st.warning("No files available in this category.")

# Contact Me Page
elif page == "Contact Me":
    st.title("Contact Information")
    st.write("📧 Email: m.asdz@yahoo.com")
