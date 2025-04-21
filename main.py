import streamlit as st
import pandas as pd
import os
from io import BytesIO

# این خط باید اولین دستور باشد
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
    "gasti": "Gasti"  # اصلاح نام دسته‌بندی (کلید کوچک، مقدار اصلی بزرگ)
}

# Ensure main folders exist
for folder in CATEGORY_FOLDERS.values():
    os.makedirs(folder, exist_ok=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Upload", "Archive", "Contact Me"])

# Home Page
if page == "Home":
    st.title("Welcome to the Data Management App")
    st.write("Use the sidebar to navigate.")

# Upload Page
elif page == "Upload":
    st.title("Upload Files")
    st.write("Upload your daily Excel files.")

    # File uploader
    uploaded_files = st.file_uploader("Upload Excel files", type=["xlsx"], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_name = uploaded_file.name.lower()  # تبدیل نام فایل به حروف کوچک
            st.subheader(f"Processing: {uploaded_file.name}...")

            # Determine category based on filename (case-insensitive)
            category = None
            for key in CATEGORY_FOLDERS:
                if key in file_name:  # بررسی بدون حساسیت به حروف بزرگ/کوچک
                    category = CATEGORY_FOLDERS[key]
                    break

            if category is None:
                st.warning(f"❌ Category not found for file: {uploaded_file.name}. Skipping...")
                continue

            # Check if file already exists
            save_path = os.path.join(category, uploaded_file.name)
            if os.path.exists(save_path):
                st.error(f"❌ File '{uploaded_file.name}' already exists in {category}! Upload skipped.")
                continue

            # Save file in the corresponding category folder
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.success(f"✅ File saved to {category}/")

    # Download Section
    st.subheader("Download Files from Archive")
    selected_category = st.selectbox("Select Category", list(CATEGORY_FOLDERS.values()))

    if selected_category:
        files = [f for f in os.listdir(selected_category) if os.path.isfile(os.path.join(selected_category, f))]

        if files:
            selected_file = st.selectbox("Select File to Download", files)

            if selected_file:
                file_path = os.path.join(selected_category, selected_file)

                with open(file_path, "rb") as f:
                    file_bytes = f.read()

                st.download_button(
                    label="Download File",
                    data=file_bytes,
                    file_name=selected_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.warning("No files available in this category.")

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

# Contact Me Page
elif page == "Contact Me":
    st.title("Contact Information")
    st.write("📧 Email: m.asdz@yahoo.com")