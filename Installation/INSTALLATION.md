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

We’ll keep all dependencies in a `requirements.txt` file located in the project root.  
For now, install the initial set of packages manually:

```bash
pip install pytest pytest-bdd pydantic playwright requests python-dotenv
```

Later, we’ll add:
- `pytest-html` or `allure-pytest` → for reports  
- `selenium` or `playwright` → for browser automation  
- `ollama` API integration packages → for LLM features  

To freeze your environment:

```bash
pip freeze > requirements.txt
```

---

## 5️⃣ Verify Installation

Run Python:

```bash
python --version
```

Run pytest (should show no errors):

```bash
pytest --version
```

---

## 6️⃣ Deactivate Environment

When done:

```bash
deactivate
```

To reactivate later, run:

```bash
.venv\Scripts\activate
```

---

✅ **Next step:**  
After finishing these steps, we’ll create the folder structure and basic `README.md` with project goals.
