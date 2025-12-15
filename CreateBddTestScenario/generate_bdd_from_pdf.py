# file: generate_bdd_from_pdf.py

import os
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import UnstructuredPDFLoader

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "Docs")

PDF_FILE = os.path.join(DOCS_DIR, "LoginDocumentation.pdf")

# ---------------------------------------------------------
# LLM MODELS
# ---------------------------------------------------------

# Model 1 → Extract & normalize requirements
draft_model = ChatOllama(
    model="gpt-oss:120b-cloud",
    temperature=0.3
)

# Model 2 → Enforce strict BDD style contract
refine_model = ChatOllama(
    model="deepseek-v3.1:671b-cloud",
    temperature=0.2
)

# ---------------------------------------------------------
# UNIVERSAL BDD PROMPT (YOUR CONTRACT)
# ---------------------------------------------------------
BDD_STYLE_PROMPT = """
You are a Behavior-Driven Development (BDD) expert.
Generate high-quality Gherkin scenarios following the STRICT style contract below.
Apply these rules consistently.

================ STYLE CONTRACT ================

- Use present-tense, imperative verbs
- One action per step
- Exactly one When per scenario
- Given → When → Then order only
- No UI implementation details
- Use semantic identifiers
- Use Background for shared Given steps
- Prefer Scenario Outline + Examples for data-driven flows
- Steps must be reusable and automation-ready

================ REQUIREMENTS ==================

{requirements}

================ OUTPUT ==================

Generate COMPLETE Gherkin feature files.
"""

# ---------------------------------------------------------
# STEP 1: READ PDF
# ---------------------------------------------------------
def load_requirements_from_pdf() -> str:
    if not os.path.exists(PDF_FILE):
        raise FileNotFoundError(f"Missing PDF file: {PDF_FILE}")

    loader = UnstructuredPDFLoader(
        file_path=PDF_FILE,
        languages=["eng"]
    )

    docs = loader.load()

    raw_text = "\n\n".join(doc.page_content.strip() for doc in docs)

    # Keep prompt-safe size
    return raw_text[:3000]

# ---------------------------------------------------------
# STEP 2: NORMALIZE REQUIREMENTS (MODEL 1)
# ---------------------------------------------------------
def extract_clean_requirements(raw_text: str) -> str:
    prompt = f"""
You are a senior QA analyst.

Extract and normalize functional requirements from the text below.
Remove noise, explanations, and formatting issues.
Keep only behavior-relevant requirements.

TEXT:
{raw_text}
"""

    response = draft_model.invoke(prompt)
    return response.content.strip()

# ---------------------------------------------------------
# STEP 3: GENERATE STRICT BDD (MODEL 2)
# ---------------------------------------------------------
def generate_bdd_from_requirements(requirements: str) -> str:
    prompt = BDD_STYLE_PROMPT.format(requirements=requirements)
    response = refine_model.invoke(prompt)
    return response.content.strip()

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
if __name__ == "__main__":
    try:
        print("📄 Reading requirements from PDF...")
        raw_requirements = load_requirements_from_pdf()

        print("🤖 Model 1: Normalizing requirements...")
        clean_requirements = extract_clean_requirements(raw_requirements)

        print("🤖 Model 2: Generating STRICT BDD scenarios...")
        bdd_output = generate_bdd_from_requirements(clean_requirements)

        print("\n🎉 GENERATED BDD SCENARIOS:\n")
        print(bdd_output)

    except Exception as e:
        print(f"❌ Error: {e}")
