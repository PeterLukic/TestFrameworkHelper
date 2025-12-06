import os
from langchain_ollama import ChatOllama

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "Docs")

BDD_FILE = os.path.join(DOCS_DIR, "BddLoginScenario.txt")
POM_FILE = os.path.join(DOCS_DIR, "PomLogin.txt")
OUTPUT_FILE = os.path.join(DOCS_DIR, "GeneratedLoginSteps.ts")

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
You are an expert QA Automation architect.

Using the following BDD scenario and POM description, generate a CLEAN, RAW draft of Playwright BDD step definitions.

DO NOT format as explanations — ONLY produce the step logic.

--- BDD ---
{bdd_content}

--- POM ---
{pom_content}

Generate only the draft step definitions with correct method names, but NO project structure and NO imports.
"""

REFINE_PROMPT_TEMPLATE = """
import {{ When, Then }} from '../../support/fixtures';
import {{ PageManager }} from '../../../pageobjects/PageManager';
import {{ PageLogin }} from '../../../pageobjects/PageLogin';
import data from '../../../utils/data.json';

type FixtureContext = {{
    pageManager: PageManager;
}};

// Steps will be generated below:
{draft}
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
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(final_steps)

print("\n🎉 DONE!")
print(f"Generated steps saved to:\n➡ {OUTPUT_FILE}")
