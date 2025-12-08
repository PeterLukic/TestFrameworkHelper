import os
from langchain_ollama import ChatOllama

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "Docs")
STEPS_DIR = os.path.join(BASE_DIR, "Steps")

BDD_FILE = os.path.join(DOCS_DIR, "BddLoginScenario.txt")
POM_FILE = os.path.join(DOCS_DIR, "PomLogin.txt")
OUTPUT_FILE = os.path.join(STEPS_DIR, "GeneratedLoginSteps.ts")

# ---------------------------------------------------------
# Load input files
# ---------------------------------------------------------
def load_file(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

bdd_content = load_file(BDD_FILE)
pom_content = load_file(POM_FILE)

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
# PROMPTS
# ---------------------------------------------------------

DRAFT_PROMPT = f"""
You are an expert QA automation architect.

Using the following BDD scenario and POM description, generate a CLEAN minimal draft
of Playwright Cucumber step definitions.

RULES:
- Do NOT invent any POM methods
- Use ONLY methods that exist in the provided POM
- Do NOT generate imports
- Do NOT generate descriptions or explanations
- Only output raw step logic (When / Then / Given blocks)

--- BDD ---
{bdd_content}

--- POM ---
{pom_content}
"""

REFINE_PROMPT_TEMPLATE = """
You are an expert TS Playwright architect.

Rewrite the following RAW draft step definitions into FINAL Cucumber step definitions
that exactly match this project structure:

REQUIREMENTS:
- Import steps EXACTLY like this:

import {{ When, Then, Given }} from '../../support/fixtures';
import {{ PageManager }} from '../../../pageobjects/PageManager';
import {{ LoginpomPage }} from '../../../pageobjects/LoginpomPage';
import data from '../../../utils/data.json';

- Use fixture context: 
  type FixtureContext = {{
      pageManager: PageManager;
  }};

- Page reference MUST be:
  const pageLogin = (pm: PageManager): LoginpomPage => pm.getLoginPage();

- Use ONLY methods existing in the POM provided earlier.

- Steps MUST be production-ready, strict, typed, valid TS.

INSERT THE DRAFT STEPS HERE:
-----------------------------------
{draft}
-----------------------------------

NOW produce the final Playwright BDD steps with imports, typing, and correct POM calls.
"""

# ---------------------------------------------------------
# RUN PIPELINE
# ---------------------------------------------------------
print("🔥 Step 1: Generating draft step definitions...")
draft_result = draft_model.invoke(DRAFT_PROMPT)
draft_text = draft_result.content.strip()

print("🔥 Step 2: Refining into real Playwright BDD steps...")
refine_prompt = REFINE_PROMPT_TEMPLATE.format(draft=draft_text)
final_result = refine_model.invoke(refine_prompt)
final_steps = final_result.content.strip()

# ---------------------------------------------------------
# SAVE OUTPUT
# ---------------------------------------------------------
os.makedirs(STEPS_DIR, exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(final_steps)

print("\n🎉 DONE!")
print(f"Generated steps saved to:\n➡ {OUTPUT_FILE}")
