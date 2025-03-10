import streamlit as st
import os
import base64
import zipfile
import fitz
from io import BytesIO
from mistralai import Mistral

st.set_page_config(layout="wide", page_title="Mistral OCR App", page_icon="🖥️")
st.title("Mistral OCR App - Max file size: 10MB")

st.markdown("<h3 style color: white;'>Built by <a href='https://github.com/AIAnytime'>AI Anytime </a></h3>", unsafe_allow_html=True)

with st.expander("Expand Me"):
    st.markdown("""
    This application allows you to extract text from PDFs/Images using Mistral OCR. Built by AI Anytime.
    """)

# Function to split PDFs into smaller parts
def split_pdf(pdf_bytes, max_pages=5):
    """
    Splits a PDF into smaller chunks of `max_pages` pages each.
    Returns a list of byte objects.
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    split_docs = []
    
    for i in range(0, len(doc), max_pages):
        new_doc = fitz.open()
        for j in range(i, min(i + max_pages, len(doc))):
            new_doc.insert_pdf(doc, from_page=j, to_page=j)
        pdf_stream = new_doc.write()
        split_docs.append(pdf_stream)
    
    return split_docs

# File size limit for Mistral API
MAX_FILE_SIZE_MB = 10

# 1. API Key Input
api_key = st.text_input("Enter your Mistral API Key", type="password")
if not api_key:
    st.info("Please enter your API key to continue.")
    st.stop()

# Initialize session state for OCR results
if "ocr_results" not in st.session_state:
    st.session_state["ocr_results"] = {}

# 2. Select file type: PDF or Image
file_type = st.radio("Select file type", ("PDF", "Image"), key="file_type_radio")

# 3. Select source type: URL or Local Upload
source_type = st.radio("Select source type", ("URL", "Local Upload"), key="source_type_radio")

# File upload handling
input_urls = []
uploaded_files = []

if source_type == "URL":
    num_urls = st.number_input("Number of URLs", min_value=1, max_value=10, step=1)
    for i in range(num_urls):
        input_urls.append(st.text_input(f"Enter URL {i+1}"))
else:
    uploaded_files = st.file_uploader(
        "Upload one or multiple files (Max 10MB each)",
        type=["pdf"] if file_type == "PDF" else ["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

# **Process Button & OCR Handling**
if st.button("Process"):
    client = Mistral(api_key=api_key)
    ocr_results = {}

    if source_type == "URL":
        for url in input_urls:
            if url:
                document = {
                    "type": "document_url" if file_type == "PDF" else "image_url",
                    "document_url" if file_type == "PDF" else "image_url": url
                }

                with st.spinner(f"Processing {url}..."):
                    ocr_response = client.ocr.process(
                        model="mistral-ocr-latest",
                        document=document,
                        include_image_base64=True
                    )
                    try:
                        pages = ocr_response.pages if hasattr(ocr_response, "pages") else ocr_response
                        result_text = "\n\n".join(page.markdown for page in pages) if pages else "No result found."
                    except Exception as e:
                        result_text = f"Error extracting result: {e}"

                    ocr_results[url] = result_text
    else:
        for uploaded_file in uploaded_files:
            file_bytes = uploaded_file.read()
            file_size_mb = len(file_bytes) / (1024 * 1024)  # Convert bytes to MB

            st.write(f"📂 **File:** {uploaded_file.name} | **Size:** {file_size_mb:.2f} MB")  

            if file_size_mb > MAX_FILE_SIZE_MB:
                st.warning(f"⚠️ File **{uploaded_file.name}** exceeds {MAX_FILE_SIZE_MB}MB. Splitting into smaller parts...")
                pdf_chunks = split_pdf(file_bytes, max_pages=5)  # Split large PDF
            else:
                pdf_chunks = [file_bytes]  # Keep as a single chunk if within limit

            for i, chunk in enumerate(pdf_chunks):
                encoded_data = base64.b64encode(chunk).decode("utf-8")
                document = {
                    "type": "document_url",
                    "document_url": f"data:application/pdf;base64,{encoded_data}"
                }

                chunk_name = f"{uploaded_file.name}_part_{i+1}"  # Unique name for each chunk
                
                with st.spinner(f"Processing {chunk_name}..."):
                    ocr_response = client.ocr.process(
                        model="mistral-ocr-latest",
                        document=document,
                        include_image_base64=True
                    )
                    try:
                        pages = ocr_response.pages if hasattr(ocr_response, "pages") else ocr_response
                        result_text = "\n\n".join(page.markdown for page in pages) if pages else "No result found."
                    except Exception as e:
                        result_text = f"Error extracting result: {e}"

                    ocr_results[chunk_name] = result_text  # Store each chunk's result separately

    st.session_state["ocr_results"] = ocr_results

# **5. Display Results & Provide Download Links**
if st.session_state["ocr_results"]:
    st.subheader("OCR Results")
    
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for filename, content in st.session_state["ocr_results"].items():
            st.write(f"📄 **{filename}**")
            st.write(content)
            file_data = content.encode()
            zip_file.writestr(f"{filename}.txt", file_data)

            # Individual file download link
            b64 = base64.b64encode(file_data).decode()
            href = f'<a href="data:file/txt;base64,{b64}" download="{filename}.txt">📥 Download {filename} OCR Result</a>'
            st.markdown(href, unsafe_allow_html=True)

    zip_buffer.seek(0)
    b64_zip = base64.b64encode(zip_buffer.read()).decode()
    zip_href = f'<a href="data:application/zip;base64,{b64_zip}" download="ocr_results.zip">📥 Download All Results</a>'
    st.markdown(zip_href, unsafe_allow_html=True)
