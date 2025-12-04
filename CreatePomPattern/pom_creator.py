# file: pom_creator.py

import os
import re
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama

# --- LLM Configuration ---
llm = ChatOllama(
    model="deepseek-v3.1:671b-cloud",
    base_url="http://localhost:11434",
    temperature=0.2
)

# --- Extract a useful class name from filename (optional enhancement) ---
def infer_class_name(file_path: str) -> str:
    raw = os.path.basename(file_path).replace(".txt", "").lower()
    raw = re.sub(r'[^a-zA-Z0-9]', ' ', raw)
    words = raw.split()
    if not words:
        return "GeneratedPage"
    return "".join(w.capitalize() for w in words) + "Page"


# --- UNIVERSAL POM PROMPT TEMPLATE ---
pom_prompt = PromptTemplate(
    input_variables=["page_description", "mode", "class_name"],
    template="""
You are an expert QA Automation Engineer specializing in building enterprise-grade Playwright automation frameworks.

Your task: **Generate a complete and production-ready Playwright Page Object Model (POM) class in TypeScript**.

### STRICT REQUIREMENTS:
- Output **ONLY TypeScript code**.
- No markdown, no comments, no explanations, no backticks.
- Use this class name: {class_name}
- The structure MUST follow this exact high-quality template:

==================================================
import {{ Page, Locator, expect }} from '@playwright/test';

export class {class_name} {{
    readonly page: Page;

    // Locators
    // (Auto-generate all relevant locators)

    constructor(page: Page) {{
        this.page = page;

        // Initialize all locators using page.locator()
    }}

    async goto(url: string): Promise<void> {{
        await this.page.goto(url);
    }}

    async waitForPageLoad(): Promise<void> {{
        await this.page.waitForLoadState('networkidle');
    }}

    // Form Actions
    // (fill, click, clear, select, uploads, shortcuts, etc.)

    // Composite Actions
    // (Multi-step user flows)

    // Verification Methods
    // (isVisible, verifyText, verifyTitle, verifyElementPresent)

    // Utility Methods
    // (getText, getValue, isEnabled, getPlaceholder, etc.)
}}
==================================================

### Requirements for generated POM:
1. All locators must use **page.locator()**.
2. Locator names must be **semantic camelCase**.
3. Extract all inputs, buttons, links, labels, headings, icons, errors, messages.
4. Build meaningful helper methods for:
   - Form actions
   - Clicks & fills
   - Composite actions (login, submitForm, search, saveChanges, etc.)
   - Verification methods (visibility, text match, enabled state)
   - Utility accessors (getText, getValue, getPlaceholder)
5. The code must be **ready to copy-paste into a real Playwright project**.
6. No extra explanations. Only clean TypeScript code.

### Mode:
{mode}

### Page or HTML Content:
{page_description}

Generate the full POM now:
"""
)

# --- Load HTML or description ---
file_path = "./Docs/LoginPom.txt"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"{file_path} not found.")

with open(file_path, "r", encoding="utf-8") as f:
    page_description = f.read()

mode = "HTML mode" if ("<" in page_description and ">" in page_description) else "Description mode"
class_name = infer_class_name(file_path)

# --- Chain Pipeline ---
chain = pom_prompt | llm | StrOutputParser()

generated_pom = chain.invoke({
    "page_description": page_description,
    "mode": mode,
    "class_name": class_name
})

# --- Cleanup (remove markdown or mistakes) ---
bad_patterns = ["```", "**", "###", "analysis", "summary", "markdown", "Explanation", "* "]
cleaned = []
for line in generated_pom.splitlines():
    if not any(b in line for b in bad_patterns):
        cleaned.append(line)

generated_pom = "\n".join(cleaned).strip()

# --- Output ---
print("\n✅ Generated Playwright POM:\n")
print(generated_pom)

# --- Save to file ---
output_path = f"./Generated_{class_name}.ts"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(generated_pom)

print(f"\n💾 POM saved to {output_path}\n")
