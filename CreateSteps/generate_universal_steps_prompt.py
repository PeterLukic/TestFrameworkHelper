# file: generate_universal_steps_prompt.py

import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DOCS_DIR = os.path.join(BASE_DIR, "Docs")
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")

INPUT_FILE = os.path.join(DOCS_DIR, "ExistingSteps.txt")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "UniversalStepsPrompt.txt")

# Ensure Output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# LLM MODELS
# ---------------------------------------------------------

# Model 1 → Analyze existing steps
draft_model = ChatOllama(
    model="gpt-oss:120b-cloud",
    temperature=0.3
)

# Model 2 → Normalize into universal contract
refine_model = ChatOllama(
    model="deepseek-v3.1:671b-cloud",
    temperature=0.15
)

# ---------------------------------------------------------
# LOAD EXISTING STEPS
# ---------------------------------------------------------
def load_existing_steps() -> str:
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(f"Missing input file: {INPUT_FILE}")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return f.read()[:4000]  # keep prompt-safe size

# ---------------------------------------------------------
# PROMPTS
# ---------------------------------------------------------

ANALYZE_STEPS_PROMPT = """
You are a Senior QA Automation Architect.

Analyze the following existing BDD step definitions.

Extract:
- Naming conventions
- Step grammar patterns
- Parameter styles
- Reusability rules
- Action vs verification separation
- Page Object interaction rules

DO NOT rewrite steps.
DO NOT generate code.
ONLY extract structural and behavioral patterns.

EXISTING STEPS:
----------------
{steps}
----------------
"""

UNIVERSAL_STEPS_PROMPT = """
UNIVERSAL BDD STEP DEFINITIONS PROMPT

ROLE:
You generate BDD step definitions that strictly follow the rules below.

STRICT RULES:
- Given / When / Then / And only
- One action per step
- Reusable and parameterized
- No UI selectors or locators
- No navigation mixed with verification

NAMING:
- Present tense, imperative
- Domain language only
- Semantic parameter names

POM INTEGRATION:
- Steps map 1:1 to Page Object methods
- No locator exposure
- No new methods invented

PROJECT PATTERNS:
{patterns}

OUTPUT:
This prompt is used to generate consistent, automation-ready BDD steps.
"""

# ---------------------------------------------------------
# PIPELINE
# ---------------------------------------------------------
def generate_universal_steps_prompt() -> str:
    print("📄 Reading existing steps...")
    steps_text = load_existing_steps()

    print("🤖 Model 1: Extracting patterns...")
    analyze_prompt = PromptTemplate.from_template(ANALYZE_STEPS_PROMPT)
    patterns = draft_model.invoke(
        analyze_prompt.format(steps=steps_text)
    ).content.strip()

    print("🤖 Model 2: Creating universal steps prompt...")
    final_prompt = PromptTemplate.from_template(UNIVERSAL_STEPS_PROMPT)
    universal_prompt = refine_model.invoke(
        final_prompt.format(patterns=patterns)
    ).content.strip()

    return universal_prompt

# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------
if __name__ == "__main__":
    try:
        result = generate_universal_steps_prompt()

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(result)

        print("\n✅ Universal Steps Prompt generated successfully")
        print(f"💾 Saved to: {OUTPUT_FILE}\n")

    except Exception as e:
        print(f"❌ Error: {e}")

