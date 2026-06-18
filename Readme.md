# 📄 AI Document Analyzer

AI Document Analyzer is a Streamlit-based application that allows users to upload or paste documents, generate AI-powered summaries, and rewrite content in different tones using local Ollama models.

## Features

* Generate concise summaries of documents
* Rewrite content in multiple tones:

  * Professional
  * Formal
  * Casual
  * Executive
  * Technical
  * Academic
  * Marketing
  * Simple English
* Support for multiple file formats:

  * PDF (.pdf)
  * Word Documents (.docx)
  * PowerPoint Presentations (.pptx)
  * Text Files (.txt)
* Adjustable summary length:

  * Short (100–200 words)
  * Medium (300–500 words)
  * Long (700–1000 words)
* Local AI inference using Ollama
* Document preview before processing
* Streamlit-based user interface

---

## Tech Stack

* Python
* Streamlit
* Ollama
* PyPDF
* python-docx
* python-pptx

---

## Project Structure

```text
project/
│
├── main.py
├── test_main.py
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama

Download and install Ollama from:

https://ollama.com

### 4. Pull a model

Example:

```bash
ollama pull llama3
```

---

## Running the Application

Start the Streamlit application:

```bash
streamlit run main.py
```

The application will open in your browser automatically.

---

## Running Tests

Execute all test cases using pytest:

```bash
pytest test_main.py
```

---

## How It Works

1. User uploads a document or pastes text.
2. Text is extracted from the document.
3. The content is previewed.
4. Ollama generates a summary based on the selected length.
5. The summary or full document is rewritten in the selected tone.
6. Results are displayed in separate tabs.

---

## Supported Document Types

| Format | Supported |
| ------ | --------- |
| PDF    | ✅         |
| DOCX   | ✅         |
| PPTX   | ✅         |
| TXT    | ✅         |

---

## Future Improvements

* Export summary as PDF
* Download rewritten content
* Multiple model comparison
* RAG-based document querying
* OCR support for scanned PDFs
* Batch document processing

---

## Author

Krish Jindal

GenAI Internship Project

