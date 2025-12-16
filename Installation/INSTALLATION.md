# 🧩 TestFrameworkHelper – Installation Guide

This guide describes how to set up the Python environment for **TestFrameworkHelper** on a Windows system.

---

## 📋 Overview

TestFrameworkHelper is an AI-powered test automation toolkit that generates:
- **BDD Test Scenarios** (Gherkin format) from PDF documentation or HTML
- **Page Object Models** (TypeScript/Playwright) from HTML structure or descriptions
- **Cucumber Step Definitions** from BDD scenarios and POM files

---

## 1️⃣ Prerequisites

Before you start, make sure you have:

- **Python 3.12.6 or higher** installed  
  👉 [Download from python.org](https://www.python.org/downloads/)
- **pip** (comes with Python by default)
- **Git** (optional, for version control)
- **Visual Studio Code** or **PyCharm** (recommended IDE)
- **Ollama** running locally at `http://localhost:11434`  
  👉 [Download from ollama.com](https://ollama.com/)

---

## 2️⃣ Create a Virtual Environment

Open a command prompt or terminal inside your project folder:

```bash
cd /path/to/TestFrameworkHelper
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

If you see `(.venv)` at the beginning of your command line — the environment is active ✅

---

## 3️⃣ Upgrade pip (recommended)

```bash
python -m pip install --upgrade pip
```

---

## 4️⃣ Install Required Packages

### Core LangChain Dependencies

```bash
pip install langchain
pip install langchain-core
pip install langchain-ollama
pip install langchain-community
pip install langchain-anthropic
```

### Document Processing

For reading and processing PDF files:

```bash
pip install unstructured
```

### Optional: Testing Framework

If you plan to use pytest for testing your generated code:

```bash
pip install pytest
pip install pytest-bdd
pip install pydantic
```

### Optional: Jupyter Notebook Support

If you want to use the Jupyter notebooks included in the project:

```bash
pip install notebook
pip install ipykernel
```

---

## 5️⃣ Install All Dependencies at Once

Alternatively, create a `requirements.txt` file with the following content:

```txt
langchain
langchain-core
langchain-ollama
langchain-community
langchain-anthropic
unstructured
```

Then install all dependencies:

```bash
pip install -r requirements.txt
```

---

## 6️⃣ Install Ollama Models

After installing Ollama, pull the required models used in this project:

### Required Models
```bash
ollama pull deepseek-v3.1:671b-cloud
ollama pull gpt-oss:120b-cloud
```

### Optional Models (for experimentation)
```bash
ollama pull llama3.2
ollama pull qwen2.5
ollama pull gemma3:12b
```

---

## 7️⃣ Set Up Anthropic API Key (Optional)

If you want to use Claude AI (used in some notebooks), set your API key:

**Option 1: Environment Variable**
```bash
export ANTHROPIC_API_KEY="your_api_key_here"  # macOS/Linux
set ANTHROPIC_API_KEY="your_api_key_here"     # Windows
```

**Option 2: In Python Code**
```python
import os
os.environ["ANTHROPIC_API_KEY"] = "your_api_key_here"
```

---

## 8️⃣ Verify Installation

### Check Python Version
```bash
python --version
# Should show 3.12.6 or higher
```

### Test LangChain Import
```bash
python -c "from langchain_ollama import ChatOllama; print('✅ LangChain Ollama installed successfully')"
```

### Test Unstructured Import
```bash
python -c "from langchain_community.document_loaders import UnstructuredPDFLoader; print('✅ Unstructured installed successfully')"
```

### Test Ollama Connection
```bash
python -c "from langchain_ollama import ChatOllama; llm = ChatOllama(model='gpt-oss:120b-cloud'); print('✅ Ollama connection successful')"
```

---

## 9️⃣ Project Structure

Your project should have the following structure:

```
TestFrameworkHelper/
├── .venv/                                    # Virtual environment (excluded from git)
├── .gitignore
├── CreateBddTestScenario/
│   ├── Docs/
│   │   ├── ExistingBDD.txt                  # Example BDD scenarios
│   │   ├── HtmlStructure.txt                # HTML for BDD generation
│   │   └── LoginDocumentation.pdf           # PDF requirements
│   ├── Output/
│   │   ├── BddStyleContract.txt             # BDD style rules
│   │   ├── GeneratedBDD_FromHtml.feature    # Generated output
│   │   └── UniversalBddPrompt.txt           # BDD prompt template
│   ├── BddTestCaseCreator.ipynb             # Jupyter notebook
│   ├── generate_bdd_from_html.py            # HTML → BDD generator
│   ├── generate_bdd_from_pdf.py             # PDF → BDD generator
│   ├── generate_bdd_login.py                # Login BDD generator
│   └── generate_bdd_template.py             # Template generator
├── CreatePomPattern/
│   ├── Docs/
│   │   ├── ExistingPOM.txt                  # Example POM files
│   │   ├── Login.txt                        # HTML for POM generation
│   │   └── ParsedLoginPage.txt              # Parsed element data
│   ├── Output/
│   │   ├── PageLogin.ts                     # Generated POM
│   │   └── UniversalPomPrompt.txt           # POM prompt template
│   ├── generate_pom_prompt.py               # POM generator
│   └── pom_creator.py                       # POM creator
├── CreateSteps/
│   ├── Docs/
│   │   ├── BddLoginScenario.txt             # BDD scenarios for steps
│   │   └── PomLogin.txt                     # POM for step generation
│   ├── Steps/
│   │   └── GeneratedLoginSteps.ts           # Generated output
│   └── generate_bdd_login_steps.py          # Step definition generator
├── Installation/
│   └── INSTALLATION.md                      # This file
└── requirements.txt                         # Python dependencies
```

---

## 🔟 Usage Examples

### Generate BDD Test Cases from PDF

```bash
cd CreateBddTestScenario
python generate_bdd_from_pdf.py
```

**Input:** `Docs/LoginDocumentation.pdf`  
**Output:** `Output/GeneratedBDD_FromPdf.feature`

### Generate BDD Test Cases from HTML

```bash
cd CreateBddTestScenario
python generate_bdd_from_html.py
```

**Input:** `Docs/HtmlStructure.txt`  
**Output:** `Output/GeneratedBDD_FromHtml.feature`

### Generate Page Object Model

```bash
cd CreatePomPattern
python pom_creator.py
```

**Input:** `Docs/Login.txt`  
**Output:** `Output/PageLogin.ts`

### Generate Cucumber Step Definitions

```bash
cd CreateSteps
python generate_bdd_login_steps.py
```

**Input:** `Docs/BddLoginScenario.txt` + `Docs/PomLogin.txt`  
**Output:** `Steps/GeneratedLoginSteps.ts`

---

## 1️⃣1️⃣ Working with Jupyter Notebooks

Start Jupyter:

```bash
jupyter notebook
```

Open `CreateBddTestScenario/BddTestCaseCreator.ipynb` to experiment with BDD generation interactively.

---

## 1️⃣2️⃣ Deactivate Environment

When done working:

```bash
deactivate
```

To reactivate later:

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

---

## 📦 Complete Package Reference

### Core Dependencies
| Package | Purpose |
|---------|---------|
| `langchain` | Core LLM orchestration framework |
| `langchain-core` | Core LangChain components |
| `langchain-ollama` | Ollama LLM integration |
| `langchain-community` | Community tools (document loaders) |
| `langchain-anthropic` | Claude AI integration |
| `unstructured` | PDF and document processing |

### Optional Dependencies
| Package | Purpose |
|---------|---------|
| `notebook` | Jupyter notebook support |
| `ipykernel` | Jupyter kernel |
| `pytest` | Testing framework |
| `pytest-bdd` | BDD testing support |
| `pydantic` | Data validation |

---

## 🔧 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'langchain_ollama'`
**Solution:**
```bash
pip install langchain-ollama
```

### Issue: `Connection refused to http://localhost:11434`
**Solution:**
1. Make sure Ollama is running: `ollama serve`
2. Check if models are installed: `ollama list`
3. Test with: `ollama run gpt-oss:120b-cloud "Hello"`

### Issue: PDF processing fails
**Solution:**
```bash
pip install --upgrade unstructured
```

### Issue: `_token` CSRF errors in HTML parsing
**Solution:** This is expected in the HTML structure files. The generators handle this automatically.

---

## 🚀 Quick Start Workflow

1. **Install everything:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # or source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Install Ollama models:**
   ```bash
   ollama pull deepseek-v3.1:671b-cloud
   ollama pull gpt-oss:120b-cloud
   ```

3. **Test BDD generation:**
   ```bash
   cd CreateBddTestScenario
   python generate_bdd_login.py
   ```

4. **Test POM generation:**
   ```bash
   cd ../CreatePomPattern
   python pom_creator.py
   ```

---

## 📝 Configuration Notes

### Model Selection

The project uses a **two-model pipeline** approach:

1. **Draft Model** (`gpt-oss:120b-cloud`): Fast, creative generation
2. **Refine Model** (`deepseek-v3.1:671b-cloud`): Strict formatting and validation

You can modify model selection in each script:

```python
draft_model = ChatOllama(
    model="gpt-oss:120b-cloud",
    temperature=0.3
)

refine_model = ChatOllama(
    model="deepseek-v3.1:671b-cloud",
    temperature=0.2
)
```

### Temperature Settings

- **0.1-0.2**: Strict, deterministic output (refinement)
- **0.3-0.5**: Balanced creativity and consistency (drafting)

---

## ✅ Verification Checklist

- [ ] Python 3.12.6+ installed
- [ ] Virtual environment created and activated
- [ ] All pip packages installed
- [ ] Ollama installed and running
- [ ] Required models pulled (deepseek-v3.1, gpt-oss)
- [ ] Test imports successful
- [ ] Sample script runs without errors

---

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Ensure Ollama is running: `ollama list`
4. Check model availability: `ollama show gpt-oss:120b-cloud`

---

**✅ Installation Complete!**  
Your TestFrameworkHelper environment is ready for AI-powered test automation generation.