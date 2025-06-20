# pages/upload.py
import streamlit as st

def app():
    st.title("📄 Upload Notes")
    st.write("Upload your academic notes here to extract text.")

    # File uploader component
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        file_details = {
            "filename": uploaded_file.name,
            "filetype": uploaded_file.type,
            "filesize": uploaded_file.size
        }
        st.write(file_details)

        # Example: if you want to read a TXT file
        if uploaded_file.type == "text/plain":
            content = uploaded_file.read().decode("utf-8")
            st.text_area("File Content", content, height=300)

        # Example: if you want to read a PDF
        elif uploaded_file.type == "application/pdf":
            from PyPDF2 import PdfReader
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            st.text_area("File Content", text, height=300)

        # Example: if you want to read a DOCX
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            from docx import Document
            doc = Document(uploaded_file)
            text = "\n".join([para.text for para in doc.paragraphs])
            st.text_area("File Content", text, height=300)

