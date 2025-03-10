# Mistral-Scanner - From the work of AIAnytime
Original creator here - https://github.com/AIAnytime/Mistral-OCR-App/tree/main

## Overview
Mistral Scanner is a Streamlit-based application that allows users to upload PDF or image files and extract text using Mistral's OCR API. It supports **multiple file uploads**, **PDF splitting for large files**, and **text extraction from URLs**.

---


## 🎯 Features
✔ Supports **multiple file uploads** (PDF, JPG, PNG)  
✔ **Splits large PDFs** (>10MB) into smaller parts for processing  
✔ Extracts **text from URLs** and **local files**  
✔ **Downloads extracted text** as individual files or a ZIP archive  
✔ Streamlit-based UI for **ease of use**  

---

## 🚀 Steps to Install and Run

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/csb21jb/Mistral-Scanner.git
cd Mistral-Scanner
```

---

### 2️⃣ Create and Activate a Virtual Environment (Optional but Recommended)

#### **On macOS/Linux**
```bash
# If you don't have the Python virtual environment package installed:
sudo apt install python3.12-venv

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

#### **On Windows**
```powershell
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run the Application
```bash
streamlit run main.py
```

---

## 🛠 Troubleshooting
- **WebSocket errors?** Restart Streamlit: `CTRL+C`, then `streamlit run main.py`
- **Missing dependencies?** Run: `pip install -r requirements.txt` to reinstall.

