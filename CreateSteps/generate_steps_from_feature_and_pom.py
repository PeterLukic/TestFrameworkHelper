# file: generate_steps_from_feature_and_pom.py

import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DOCS_DIR = os.path.join(BASE_DIR, "Docs")
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")

FEATURE_FILE = os.path.join(DOCS_DIR, "GeneratedBDD_FromHtml.feature")
POM_FILE = os.path.join(DOCS_DIR, "PageLogin.ts")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "GeneratedSteps.ts")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# LLM MODELS
# ---------------------------------------------------------

# Model 1 → Analyze BDD + POM (structure & intent)
draft_model = ChatOllama(
    model="gpt-oss:120b-cloud",
    temperature=0.3
)

# Model 2 → Generate STRICT step definitions (framework-compliant)
refine_model = ChatOllama(
    model="deepseek-v3.1:671b-cloud",
    temperature=0.1
)

# ---------------------------------------------------------
# LOAD FILES
# ---------------------------------------------------------
def load_file(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()[:5000]

# ---------------------------------------------------------
# PROMPTS
# ---------------------------------------------------------

ANALYZE_PROMPT = """
You are a Senior QA Automation Architect.

Analyze the following inputs:

1. Gherkin Feature File
2. Existing Playwright Page Object Model (TypeScript)

Your responsibilities:
- Identify step intentions from the feature
- Identify AVAILABLE methods from the Page Object
- Define valid step → method mappings
- Identify reusable step patterns
- DO NOT invent methods
- DO NOT generate code

ONLY OUTPUT:
- Navigation step intents
- Action step intents
- Verification step intents
- Valid mapping rules

FEATURE FILE:
----------------
{feature}
----------------

PAGE OBJECT:
----------------
{pom}
----------------
"""

GENERATE_STEPS_PROMPT = """
You are a Senior QA Automation Engineer generating Playwright + Cucumber step definitions.

You MUST strictly follow this framework contract.

==================== FRAMEWORK CONTRACT ====================

1. Imports
- ALWAYS import steps from '../../support/fixtures'
- NEVER import from '@cucumber/cucumber'
- NEVER import expect from Playwright

Example:
import { Given, When, Then } from '../../support/fixtures';

2. Context Injection
- ALL steps MUST use fixture-based injection
- Arrow functions ONLY

MANDATORY signature:
async ({ pageManager }: FixtureContext, ...params) => { }

3. FixtureContext
Assume this type exists:
type FixtureContext = {
  pageManager: PageManager;
};

4. Page Object Access
- NEVER access Page Objects statically
- ALWAYS use accessor functions

Example:
const pageLogin = (pageManager: PageManager): PageLogin =>
  pageManager.getPageLogin();

5. Method Usage
- Use ONLY methods that exist in the Page Object
- DO NOT invent new methods
- Prefer composite methods when available

6. Step Rules
- One action per step
- No assertions in When steps
- Assertions ONLY in Then steps
- NO locators
- NO waits
- NO expect()
- NO implementation details

7. Naming Rules
- Short, reusable step text
- Domain language only
- Use {string} placeholders only

8. Output Rules
- Output ONLY TypeScript code
- NO markdown
- NO comments
- NO explanations
- Single file output

==================== INPUT ====================

STEP MAPPING SPECIFICATION:
{analysis}

==================== OUTPUT ====================

Generate STRICT, framework-compliant step definitions now.
"""

# ---------------------------------------------------------
# PIPELINE
# ---------------------------------------------------------
def generate_steps() -> str:
    print("📄 Loading feature and Page Object...")
    feature_text = load_file(FEATURE_FILE)
    pom_text = load_file(POM_FILE)

    print("🤖 Model 1: Analyzing step intent & mappings...")
    analyze_prompt = PromptTemplate.from_template(ANALYZE_PROMPT)
    analysis = draft_model.invoke(
        analyze_prompt.format(
            feature=feature_text,
            pom=pom_text
        )
    ).content.strip()

    print("🤖 Model 2: Generating STRICT step definitions...")
    generate_prompt = PromptTemplate.from_template(GENERATE_STEPS_PROMPT)
    steps_code = refine_model.invoke(
        generate_prompt.format(analysis=analysis)
    ).content.strip()

    # Safety cleanup
    for banned in ["```", "Explanation", "analysis", "markdown"]:
        steps_code = steps_code.replace(banned, "")

    return steps_code.strip()

# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------
if __name__ == "__main__":
    try:
        steps = generate_steps()

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(steps)

        print("\n✅ Step definitions generated successfully")
        print(f"💾 Saved to: {OUTPUT_FILE}\n")

    except Exception as e:
        print(f"❌ Error: {e}")

