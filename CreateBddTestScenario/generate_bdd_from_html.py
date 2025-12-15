# file: generate_bdd_from_html.py

import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DOCS_DIR = os.path.join(BASE_DIR, "Docs")
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")

HTML_FILE = os.path.join(DOCS_DIR, "HtmlStructure.txt")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "GeneratedBDD_FromHtml.feature")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# LLM MODELS
# ---------------------------------------------------------
draft_model = ChatOllama(
    model="gpt-oss:120b-cloud",
    temperature=0.3
)

refine_model = ChatOllama(
    model="deepseek-v3.1:671b-cloud",
    temperature=0.2
)

# ---------------------------------------------------------
# LOAD HTML STRUCTURE
# ---------------------------------------------------------
def load_html_structure(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing HTML structure file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# ---------------------------------------------------------
# PROMPTS
# ---------------------------------------------------------
ANALYZE_HTML_PROMPT = """
You are a QA Automation Architect.

Analyze the following HTML or DOM structure and extract:
- User-visible pages or components
- Possible user actions
- Valid interaction flows
- Invalid and edge-case behaviors
- Business-relevant user intent

DO NOT write Gherkin.
DO NOT write code.
ONLY describe behavioral intent in clear text.

HTML STRUCTURE:
----------------
{html}
----------------
"""

STRICT_BDD_PROMPT = """
# BDD Scenario Generator Prompt

## Instructions
You are a Behavior-Driven Development (BDD) expert. Generate high-quality Gherkin scenarios following the strict style contract below. Apply these rules consistently.

## STRICT STYLE CONTRACT
[PASTE YOUR FULL BDD CONTRACT HERE EXACTLY AS DEFINED]

## INPUT BEHAVIOR DESCRIPTION
{behavior}

## OUTPUT
Generate complete, clean Gherkin feature files.
"""

# ---------------------------------------------------------
# PIPELINE
# ---------------------------------------------------------
def generate_bdd_from_html() -> str:
    print("📄 Reading HTML structure...")
    html_text = load_html_structure(HTML_FILE)[:3000]

    print("🤖 Step 1: Extracting behavior intent (Model 1)...")
    analyze_prompt = PromptTemplate.from_template(ANALYZE_HTML_PROMPT)
    analyze_input = analyze_prompt.format(html=html_text)
    behavior_description = draft_model.invoke(analyze_input).content

    print("🤖 Step 2: Generating STRICT BDD scenarios (Model 2)...")
    bdd_prompt = PromptTemplate.from_template(STRICT_BDD_PROMPT)
    final_prompt = bdd_prompt.format(behavior=behavior_description)
    final_bdd = refine_model.invoke(final_prompt).content

    return final_bdd.strip()

# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------
if __name__ == "__main__":
    try:
        result = generate_bdd_from_html()

        print("\n🎉 GENERATED BDD FROM HTML STRUCTURE:\n")
        print(result)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"\n💾 BDD saved to: {OUTPUT_FILE}\n")

    except Exception as e:
        print(f"❌ Error: {e}")
