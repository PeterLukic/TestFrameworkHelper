# 🧩 TestFrameworkHelper – Installation Guide

This guide describes how to set up the Python environment for **TestFrameworkHelper** on a Windows system.

---

## 1️⃣ Prerequisites

Before you start, make sure you have:

- **Python 3.11 or higher** installed  
  👉 [Download from python.org](https://www.python.org/downloads/)
- **pip** (comes with Python by default)
- **Git** (optional, for version control)
- **Visual Studio Code** or **PyCharm** (recommended IDE)
- **Ollama** running locally at `http://localhost:11434`  
  👉 [Download from ollama.com](https://ollama.com/)

---

## 2️⃣ Create a Virtual Environment

Open a command prompt inside your project folder:

```bash
cd C:\Users\Korisnik\Documents\Learning\TestFrameworkHelper
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it (Windows):

```bash
.venv\Scripts\activate
```

If you see `(.venv)` at the beginning of your command line — the environment is active ✅

---

## 3️⃣ Upgrade pip (recommended)

```bash
python -m pip install --upgrade pip
```

---

## 4️⃣ Install Required Packages

### Core Dependencies

Install the main packages needed for the project:

```bash
pip install langchain langchain-core langchain-ollama langchain-community langchain-anthropic
```

### Document Processing

For reading and processing PDF files:

```bash
pip install unstructured
```

### Testing Framework (Optional)

If you plan to use pytest for testing:

```bash
pip install pytest pytest-bdd pydantic playwright requests python-dotenv
```

### Jupyter Notebook Support (Optional)

If you want to use Jupyter notebooks:

```bash
pip install notebook ipykernel
```

---

## 5️⃣ Install Ollama Models

After installing Ollama, pull the required models:

```bash
ollama pull qwen2.5
ollama pull llama3.2
ollama pull gemma3:12b
ollama pull deepseek-v3.1:671b-cloud
ollama pull gpt-oss:120b-cloud
ollama pull embeddinggemma
```

---

## 6️⃣ Set Up Anthropic API Key (Optional)

If you want to use Claude AI, create a `.env` file in the project root:

```bash
ANTHROPIC_API_KEY=your_api_key_here
```

Or set it directly in your scripts (as shown in the notebooks).

---

## 7️⃣ Create requirements.txt

Save all dependencies to a file:

```bash
pip freeze > requirements.txt
```

To install from `requirements.txt` later:

```bash
pip install -r requirements.txt
```

---

## 8️⃣ Verify Installation

Run Python:

```bash
python --version
```

Test LangChain import:

```bash
python -c "from langchain_ollama import ChatOllama; print('✅ LangChain installed successfully')"
```

Test Unstructured import:

```bash
python -c "from langchain_community.document_loaders import UnstructuredPDFLoader; print('✅ Unstructured installed successfully')"
```

---

## 9️⃣ Project Structure

Ensure your project has the following structure:

```
TestFrameworkHelper/
├── .venv/                          # Virtual environment
├── CreateBddTestScenario/
│   ├── Docs/
│   │   └── LoginDocumentation.pdf  # Your PDF requirements
│   ├── BddTestCaseCreator.ipynb
│   ├── generate_bdd_from_pdf.py
│   └── generate_bdd_login.py
├── CreatePomPattern/
│   ├── Docs/
│   │   ├── LoginPom.txt
│   │   └── ParsedLoginPage.txt
│   ├── PomCreator.ipynb
│   ├── pom_creator.py
│   └── Generated_LoginpomPage.ts
├── Installation/
│   └── INSTALLATION.md             # This file
├── .gitignore
└── requirements.txt
```

---

## 🔟 Deactivate Environment

When done:

```bash
deactivate
```

To reactivate later, run:

```bash
.venv\Scripts\activate
```

---

## 📦 Complete Package List

Here's the full list of packages used in this project:

### LLM & LangChain Integration
- `langchain` - Core LangChain library
- `langchain-core` - Core components
- `langchain-ollama` - Ollama LLM integration
- `langchain-community` - Community tools (document loaders)
- `langchain-anthropic` - Claude AI integration (optional)

### Document Processing
- `unstructured` - PDF and document processing

### Testing (Optional)
- `pytest` - Testing framework
- `pytest-bdd` - BDD testing
- `pydantic` - Data validation
- `playwright` - Browser automation
- `requests` - HTTP library
- `python-dotenv` - Environment variables

### Development Tools (Optional)
- `notebook` - Jupyter notebook support
- `ipykernel` - Jupyter kernel

---

## 🚀 Quick Start

After installation, you can run:

**Generate BDD test cases from PDF:**
```bash
python CreateBddTestScenario/generate_bdd_login.py
```

**Generate POM pattern from HTML:**
```bash
python CreatePomPattern/pom_creator.py
```

**Run Jupyter notebooks:**
```bash
jupyter notebook
```

---

✅ **You're all set!**  
Your TestFrameworkHelper environment is ready for BDD test generation and POM pattern creation.