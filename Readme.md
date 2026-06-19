# Document Summarizer and Rewriter

## Overview

Document Summarizer and Rewriter is a Generative AI-powered application that analyzes documents and generates concise summaries and rewritten content in multiple communication styles. The application supports both a graphical user interface (GUI) through Streamlit and a command-line interface (CLI), providing flexibility for different user workflows.

This project was developed as part of a GenAI Internship Project.

---

## Features

### Document Processing

* Upload and analyze PDF documents
* Upload and analyze DOCX documents
* Upload and analyze PPTX documents
* Upload and analyze TXT documents
* Direct text input support

### AI-Powered Summarization

* Short Summary (100–200 words)
* Medium Summary (300–500 words)
* Long Summary (700–1000 words)
* Preservation of key information and critical insights

### Content Rewriting

Supports multiple writing styles:

* Professional
* Formal
* Casual
* Executive
* Technical
* Academic
* Marketing
* Simple English

### User Interfaces

* Streamlit-based graphical interface
* Command-line interface (CLI)

### Local AI Processing

* Uses locally hosted Ollama models
* No dependency on cloud-based AI services
* Improved privacy and control over document data

---

## Technology Stack

### Frontend

* Streamlit

### Backend

* Python

### AI Framework

* Ollama

### Document Processing Libraries

* pypdf
* python-docx
* python-pptx

### Testing

* pytest
* unittest.mock

---

## Project Structure

```text
GenAi/
│
├── app.py
├── cli.py
├── requirements.txt
│
├── core/
│   |
│   ├── analyzer.py
│   ├── extractor.py
│   └── ollama_client.py
│
├── tests/
│   ├── test_analyzer.py
│   ├── test_extractor.py
│   └── test_ollama_client.py
│
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd GenAi
```

### Create Virtual Environment

```bash
python -m venv streamlit_env
```

### Activate Environment

Linux/macOS:

```bash
source streamlit_env/bin/activate
```

Windows:

```bash
streamlit_env\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running Ollama

Ensure Ollama is installed and running.

To pull Model into local System:
```bash
ollama pull [Model Name]
```
View available models:
```bash
ollama list
```

Example model:

```bash
llama3.2:3b
```

---

## Running the Streamlit Application

```bash
streamlit run app.py
```

---

## Running the CLI Application

### Generate Summary

```bash
python cli.py summarize \
--text "Machine learning is a subset of artificial intelligence." \
--model llama3.2:3b \
--length short
```

### Rewrite Content

```bash
python cli.py rewrite \
--text "Machine learning is a subset of artificial intelligence." \
--model llama3.2:3b \
--tone Professional
```

### Analyze a Document

```bash
python cli.py summarize \
--file-path sample.pdf \
--model llama3.2:3b \
--length medium
```

---

## Running Tests

Run all tests:

```bash
python -m pytest
```

Verbose output:

```bash
python -m pytest -v
```

Coverage report:

```bash
python -m pytest --cov=core
```

---

## Future Enhancements

* Batch document processing
* Export summaries to DOCX and PDF
* Processing history tracking
* Additional language support
* Advanced document analytics
* RAG-based knowledge integration

---

## Author

Krish Jindal

GenAI Internship Project
