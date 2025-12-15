import os
from langchain_ollama import ChatOllama

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "Docs")
OUTPUT_DIR = os.path.join(BASE_DIR, "Output")

BDD_FILE = os.path.join(DOCS_DIR, "ExistingBDD.txt")
STYLE_OUTPUT = os.path.join(OUTPUT_DIR, "BddStyleContract.txt")
PROMPT_OUTPUT = os.path.join(OUTPUT_DIR, "UniversalBddPrompt.txt")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# Load BDD
# ---------------------------------------------------------
def load_file(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing file: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

bdd_content = load_file(BDD_FILE)

# ---------------------------------------------------------
# MODELS
# ---------------------------------------------------------

# Model 1: disciplined, analytical
style_model = ChatOllama(
    model="gpt-oss:120b-cloud",
    temperature=0.2
)

# Model 2: creative architect
prompt_model = ChatOllama(
    model="deepseek-v3.1:671b-cloud",
    temperature=0.1
)

# ---------------------------------------------------------
# PROMPTS
# ---------------------------------------------------------

STYLE_EXTRACTION_PROMPT = f"""
You are a senior QA architect.

Analyze the following BDD scenarios and extract a
STRICT, REUSABLE BDD STYLE CONTRACT.

Output ONLY rules.
NO explanations.
NO examples.

Rules should cover:
- Step wording
- Given / When / Then usage
- Reusability principles
- Naming conventions
- What to avoid
- Scenario structure

--- BDD INPUT ---
{bdd_content}
"""

UNIVERSAL_PROMPT_TEMPLATE = """
You are an expert BDD generator.

Using the following BDD STYLE CONTRACT,
generate a UNIVERSAL PROMPT that can be used
to generate high-quality BDD scenarios
for ANY web application page.

The prompt MUST:
- Enforce the style rules
- Be reusable across all features
- Accept feature description as input
- Produce clean, maintainable BDD

--- BDD STYLE CONTRACT ---
{style_rules}

OUTPUT:
A SINGLE reusable prompt (ready to be copy-pasted).
"""

# ---------------------------------------------------------
# PIPELINE
# ---------------------------------------------------------
print("🔥 Step 1: Extracting BDD style rules...")
style_result = style_model.invoke(STYLE_EXTRACTION_PROMPT)
style_rules = style_result.content.strip()

with open(STYLE_OUTPUT, "w", encoding="utf-8") as f:
    f.write(style_rules)

print("🔥 Step 2: Generating UNIVERSAL BDD prompt...")
universal_prompt = UNIVERSAL_PROMPT_TEMPLATE.format(style_rules=style_rules)
prompt_result = prompt_model.invoke(universal_prompt)
final_prompt = prompt_result.content.strip()

with open(PROMPT_OUTPUT, "w", encoding="utf-8") as f:
    f.write(final_prompt)

# ---------------------------------------------------------
# DONE
# ---------------------------------------------------------
print("\n🎉 DONE!")
print("✔ BDD Style Contract saved to:", STYLE_OUTPUT)
print("✔ Universal BDD Prompt saved to:", PROMPT_OUTPUT)
