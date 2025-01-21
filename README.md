# PDF and PNG Multi-ZIP Combiner Tool

This project is a Streamlit-based web application that allows users to:

1. Upload multiple ZIP files containing PDFs and PNGs.
2. Extract and display the files from the uploaded ZIPs.
3. Select specific files from the extracted contents.
4. Combine the selected files into a single PDF.
5. Store combined PDFs for download and future use.

---

## Features

- Multiple ZIP Uploads: Upload multiple ZIP files at once, each containing PDFs and PNGs.
- File Extraction: Extract and display the contents of the ZIP files in a structured manner.
- File Selection: Choose specific files (PDFs and PNGs) for combining.
- PDF Combination: Combine selected files into a single PDF file.
- Stored PDFs: Save combined PDFs on the server and make them available for download.

---

## Installation

Follow these steps to set up the project:

1. Clone the Repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install Dependencies:
   Ensure you have Python installed, then install the required libraries:
   ```bash
   pip install streamlit PyPDF2 pillow
   ```

3. Run the Application:
   Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

4. Access the App:
   Open the provided local URL (e.g., `http://localhost:8501`) in your web browser.

---

## Usage

1. Upload ZIP Files:
   - Use the file uploader to upload multiple ZIP files.
   - The app will extract and list all supported files (PDFs and PNGs).

2. Select Files:
   - Use the multi-select widget to choose specific files from the extracted list.

3. Combine Files:
   - Enter a name for the output PDF file.
   - Click the "Combine Files" button to generate the combined PDF.

4. Download Combined PDFs:
   - Download the combined PDF immediately after generation.
   - Access previously combined PDFs from the "Stored Combined PDFs" section.

---

## Directory Structure

```plaintext
project_root/
|-- app.py                  # Main application file
|-- uploaded_files/         # Directory for storing uploaded ZIPs and extracted files
|-- combined_pdfs/          # Directory for storing combined PDFs
|-- requirements.txt        # Dependencies (optional)
```

---

## Dependencies

- Streamlit: For building the web interface.
- PyPDF2: For handling PDF merging.
- Pillow: For converting PNG images to PDF.

Install them with:
```bash
pip install streamlit PyPDF2 pillow
```

---

## Future Enhancements

- Add support for more file formats (e.g., JPG, DOCX).
- Allow hierarchical display of extracted files based on folder structure.
- Implement user authentication for file security.

---

## License

This project is licensed under the MIT License. Feel free to use and modify it as needed.

---

## Contact

For questions or suggestions, please contact [your_email@example.com].

