# file: pom_creator.py

import os
import re
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

# ---------------------------------------------------------
# LLM CONFIGURATION
# ---------------------------------------------------------
llm = ChatOllama(
    model="deepseek-v3.1:671b-cloud",
    base_url="http://localhost:11434",
    temperature=0.15
)

# ---------------------------------------------------------
# CLASS NAME INFERENCE
# ---------------------------------------------------------
def infer_class_name(file_path: str) -> str:
    raw = os.path.basename(file_path).replace(".txt", "")
    raw = re.sub(r'[^a-zA-Z0-9]', ' ', raw)
    words = raw.split()
    if not words:
        return "PageGenerated"
    return "Page" + "".join(w.capitalize() for w in words)

# ---------------------------------------------------------
# UNIVERSAL BDD-DRIVEN POM PROMPT
# ---------------------------------------------------------
pom_prompt = PromptTemplate(
    input_variables=["class_name", "page_description", "mode"],
    template="""
You are a Senior QA Automation Engineer.

Generate a Playwright Page Object Model (POM) in TypeScript
that STRICTLY follows BDD-compatible architecture rules.

STRICT RULES (MANDATORY):

1. Naming:
   - Page class name: {class_name}
   - camelCase methods
   - verb-first naming

2. Method structure:
   - Navigation methods (goto, navigateToX)
   - Action methods (fillUsername, clickLoginButton)
   - Composite methods (loginWithCredentials)
   - Verification methods (verify..., assert...)
   - Boolean helpers (is..., get...)

3. Encapsulation:
   - All locators MUST be private
   - No raw locators exposed
   - No assertions inside action methods

4. Verification rules:
   - Soft checks → verify...
   - Hard expectations → assert...

5. Output rules:
   - Output ONLY TypeScript code
   - NO markdown
   - NO comments
   - NO explanations
   - Ready to paste into a real Playwright project

6. Locator rules:
   - Use page.locator()
   - Semantic camelCase names
   - Extract inputs, buttons, links, messages, errors

MODE:
{mode}

PAGE CONTENT:
{page_description}

OUTPUT:
Generate ONE Playwright Page Object class.
"""
)

# ---------------------------------------------------------
# INPUT FILE
# ---------------------------------------------------------
INPUT_FILE = "./Docs/Login.txt"
OUTPUT_DIR = "./Output"

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"{INPUT_FILE} not found")

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    page_description = f.read()

mode = "HTML mode" if "<" in page_description and ">" in page_description else "Description mode"
class_name = infer_class_name(INPUT_FILE)

# ---------------------------------------------------------
# EXECUTION PIPELINE
# ---------------------------------------------------------
chain = pom_prompt | llm | StrOutputParser()

generated_code = chain.invoke({
    "class_name": class_name,
    "page_description": page_description,
    "mode": mode
})

# ---------------------------------------------------------
# CLEANUP (SAFETY NET)
# ---------------------------------------------------------
for banned in ["```", "###", "**", "Explanation", "analysis", "markdown"]:
    generated_code = generated_code.replace(banned, "")

generated_code = generated_code.strip()

# ---------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------
output_file = os.path.join(OUTPUT_DIR, f"{class_name}.ts")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(generated_code)

print("\n✅ Playwright POM generated successfully:\n")
print(generated_code)
print(f"\n💾 Saved to: {output_file}\n")
