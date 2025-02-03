import os
import zipfile
import streamlit as st
from PyPDF2 import PdfMerger
from PIL import Image
import io
import uuid  # Import uuid module for unique user IDs

# Default directories for uploaded files and combined PDFs
DEFAULT_UPLOAD_DIR = "user_uploaded_files"
DEFAULT_COMBINED_DIR = "combined_pdfs"

# Create directories if they do not exist
os.makedirs(DEFAULT_UPLOAD_DIR, exist_ok=True)
os.makedirs(DEFAULT_COMBINED_DIR, exist_ok=True)

# Streamlit app title
st.title("PDF and PNG Multi-ZIP Combiner Tool")

# Custom location input (stored in session state)
if 'custom_dir' not in st.session_state:
    st.session_state.custom_dir = DEFAULT_UPLOAD_DIR

# Allow users to change the location of the upload directory
custom_directory = st.text_input(
    "Enter the custom file directory (Leave empty for default):", 
    value=st.session_state.custom_dir
)

# Update session state for custom directory if changed
if custom_directory.strip():
    st.session_state.custom_dir = custom_directory.strip()

# Function to get a unique directory for each user (based on session ID or UUID)
def get_user_directory():
    # Generate a unique user ID based on uuid (you could use session ID, or other methods too)
    if 'user_uid' not in st.session_state:
        # Generate a new UUID for each session
        st.session_state.user_uid = str(uuid.uuid4())  

    user_uid = st.session_state.user_uid
    user_dir = os.path.join(DEFAULT_UPLOAD_DIR, user_uid)

    # Check if the directory exists from previous sessions, otherwise create a new one
    if not os.path.exists(user_dir):
        os.makedirs(user_dir, exist_ok=True)
    
    return user_dir

# Function to extract ZIP files
def extract_zip(uploaded_zip):
    user_directory = get_user_directory()
    folder_path = os.path.join(user_directory, uploaded_zip.name.split(".")[0])
    os.makedirs(folder_path, exist_ok=True)
    with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
        zip_ref.extractall(folder_path)
    return folder_path

# Function to combine selected files into a single PDF
def combine_files(selected_files, output_filename):
    merger = PdfMerger()
    temp_images = []

    for file in selected_files:
        if file.endswith(".pdf"):
            merger.append(file)
        elif file.endswith(".png"):
            # Convert PNG to PDF
            image = Image.open(file).convert("RGB")
            temp_pdf = io.BytesIO()
            image.save(temp_pdf, format="PDF")
            temp_pdf.seek(0)
            merger.append(temp_pdf)
            temp_images.append(temp_pdf)

    # Save the combined PDF
    output_path = os.path.join(DEFAULT_COMBINED_DIR, output_filename)
    with open(output_path, "wb") as output_file:
        merger.write(output_file)

    # Cleanup temporary PDFs
    for temp_pdf in temp_images:
        temp_pdf.close()

    return output_path

# Function to list all files in the user's directory
def list_user_files():
    user_directory = get_user_directory()
    return [os.path.join(user_directory, file) for file in os.listdir(user_directory) if os.path.isfile(os.path.join(user_directory, file))]

# Function to delete a file from the user's directory
def delete_file(file_path):
    os.remove(file_path)

# File upload section
uploaded_zips = st.file_uploader("Upload ZIP files containing PDFs and PNGs", type=["zip"], accept_multiple_files=True)

all_files = []
if uploaded_zips:
    for uploaded_zip in uploaded_zips:
        folder_path = extract_zip(uploaded_zip)
        st.success(f"Extracted files from: {uploaded_zip.name}")

        # List all files in the extracted folder
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file.lower().endswith((".pdf", ".png")):
                    all_files.append(file_path)

if all_files:
    # Display all extracted files and allow user selection with checkboxes
    st.write("### Extracted Files:")

    # Create checkboxes for each file
    selected_files = []
    for file_path in all_files:
        file_name = os.path.basename(file_path)  # Only show the file name, not the full path
        if st.checkbox(file_name, key=file_path):
            selected_files.append(file_path)

    # Combine files button
    if selected_files:
        output_filename = st.text_input("Enter a name for the combined PDF (e.g., combined.pdf):", "combined.pdf")

        if st.button("Combine Files"):
            combined_pdf_path = combine_files(selected_files, output_filename)
            st.success(f"Files combined successfully! Saved as {combined_pdf_path}")

            # Display download link for the combined PDF
            with open(combined_pdf_path, "rb") as f:
                st.download_button("Download Combined PDF", f, file_name=output_filename)

# Display and allow removal of uploaded files
st.write("### Your Uploaded Files:")
user_files = list_user_files()

if user_files:
    for user_file in user_files:
        file_name = os.path.basename(user_file)
        
        # Display each file with a delete button
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(file_name)
        with col2:
            delete_button = st.button(f"Delete {file_name}", key=user_file)
            if delete_button:
                delete_file(user_file)
                st.success(f"File {file_name} has been deleted.")
                st.experimental_rerun()  # Refresh to show updated file list

else:
    st.write("No files uploaded yet.")

# Display stored combined PDFs
st.write("### Stored Combined PDFs:")
for pdf_file in os.listdir(DEFAULT_COMBINED_DIR):
    pdf_path = os.path.join(DEFAULT_COMBINED_DIR, pdf_file)
    st.write(pdf_file)
    with open(pdf_path, "rb") as f:
        st.download_button(f"Download {pdf_file}", f, file_name=pdf_file)
