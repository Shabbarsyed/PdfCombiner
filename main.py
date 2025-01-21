import os
import zipfile
import streamlit as st
from PyPDF2 import PdfMerger
from PIL import Image
import io

# Directories for uploaded files and combined PDFs
UPLOAD_DIR = "uploaded_files"
COMBINED_DIR = "combined_pdfs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(COMBINED_DIR, exist_ok=True)

# Function to extract ZIP files
def extract_zip(uploaded_zip):
    folder_path = os.path.join(UPLOAD_DIR, uploaded_zip.name.split(".")[0])
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
    output_path = os.path.join(COMBINED_DIR, output_filename)
    with open(output_path, "wb") as output_file:
        merger.write(output_file)

    # Cleanup temporary PDFs
    for temp_pdf in temp_images:
        temp_pdf.close()

    return output_path

# Streamlit app
st.title("PDF and PNG Multi-ZIP Combiner Tool")

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
    # Display all extracted files and allow user selection
    st.write("### Extracted Files:")
    selected_files = st.multiselect("Select files to combine:", all_files)

    # Combine files button
    if selected_files:
        output_filename = st.text_input("Enter a name for the combined PDF (e.g., combined.pdf):", "combined.pdf")

        if st.button("Combine Files"):
            combined_pdf_path = combine_files(selected_files, output_filename)
            st.success(f"Files combined successfully! Saved as {combined_pdf_path}")

            # Display download link for the combined PDF
            with open(combined_pdf_path, "rb") as f:
                st.download_button("Download Combined PDF", f, file_name=output_filename)

# Display stored combined PDFs
st.write("### Stored Combined PDFs:")
for pdf_file in os.listdir(COMBINED_DIR):
    pdf_path = os.path.join(COMBINED_DIR, pdf_file)
    st.write(pdf_file)
    with open(pdf_path, "rb") as f:
        st.download_button(f"Download {pdf_file}", f, file_name=pdf_file)
