# file: generate_bdd_from_pdf.py

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredPDFLoader

# ---------------------------------------------------------
#  LLM INITIALIZATION
# ---------------------------------------------------------

# ⭐ Recommended: DeepSeek Cloud – fastest + highest quality ⭐
deepseekcloud_llm = ChatOllama(
    model="deepseek-v3.1:671b-cloud",
    base_url="http://localhost:11434",
    temperature=0.5
)


# ---------------------------------------------------------
#  GENERATE MULTIPLE BDD TEST CASES
# ---------------------------------------------------------

def generate_bdd_test_cases_from_pdf(user_story: str) -> str:
    """
    Reads requirements from a PDF file and generates full BDD scenarios
    using consistent placeholders and login steps.
    """

    pdf_file = "./Docs/LoginDocumentation.pdf"
    loader = UnstructuredPDFLoader(
        file_path=pdf_file,
        languages=["eng"]
    )
    docs = loader.load()
    requirements_text = "\n\n".join([doc.page_content.strip() for doc in docs])[:2000]

    # STRICT controlled output for consistent Gherkin
    prompt_template = PromptTemplate.from_template(
        """
        You are a Senior QA Automation Engineer.

        Convert the following requirements into ALL POSSIBLE BDD test scenarios
        written in pure Gherkin syntax.

        RULES:
        - NEVER use real usernames or passwords.
        - ALWAYS use placeholders:
          "<username>", "<password>", "<invalid_username>", "<invalid_password>",
          "<empty_username>", "<empty_password>"
        - ALL login steps MUST follow exactly this structure:

            Given I open the website
            And I enter the username "<username>"
            And I enter the password "<password>"
            When I click on "Login"

        - Invalid or error scenarios MUST use:
          "<invalid_username>", "<invalid_password>", "<empty_username>", "<empty_password>"
        - Output must be pure Gherkin. No commentary.

        REQUIREMENTS:
        {requirements_text}

        FORMAT EXACTLY LIKE:

        Feature: [Feature name]

        Scenario: [Scenario name]
            Given I open the website
            And I enter the username "<username>"
            And I enter the password "<password>"
            When I click on "Login"
            Then [expected result]
        """
    )

    prompt = prompt_template.format(requirements_text=requirements_text)
    response = deepseekcloud_llm.invoke(prompt)

    return response.content if hasattr(response, "content") else str(response)


# ---------------------------------------------------------
#  GENERATE ONE BDD TEST CASE
# ---------------------------------------------------------

def generate_single_bdd_test_case_from_pdf(user_story: str) -> str:
    """
    Reads requirements from PDF and generates ONE BDD scenario
    using strict Gherkin and placeholder login steps.
    """

    pdf_file = "./Docs/LoginDocumentation.pdf"
    loader = UnstructuredPDFLoader(
        file_path=pdf_file,
        languages=["eng"]
    )
    docs = loader.load()
    requirements_text = "\n\n".join([doc.page_content.strip() for doc in docs])[:2000]

    prompt_template = PromptTemplate.from_template(
        """
        You are a Senior QA Automation Engineer.

        Convert the following requirements into ONE BDD scenario.

        RULES:
        - No real usernames or passwords.
        - ALWAYS use placeholders:
          "<username>", "<password>", "<invalid_username>", "<invalid_password>",
          "<empty_username>", "<empty_password>"
        - Login steps MUST ALWAYS begin EXACTLY like this:

            Given I open the website
            And I enter the username "<username>"
            And I enter the password "<password>"
            When I click on "Login"

        REQUIREMENTS:
        {requirements_text}

        FORMAT EXACTLY LIKE:

        Feature: [Feature name]

        Scenario: [Scenario name]
            Given I open the website
            And I enter the username "<username>"
            And I enter the password "<password>"
            When I click on "Login"
            Then [expected result]
        """
    )

    prompt = prompt_template.format(requirements_text=requirements_text)
    response = deepseekcloud_llm.invoke(prompt)

    return response.content if hasattr(response, "content") else str(response)


# ---------------------------------------------------------
#  MAIN ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    user_story_input = "Generate BDD test cases from PDF"

    try:
        # Choose one:
        # result = generate_single_bdd_test_case_from_pdf(user_story_input)
        result = generate_bdd_test_cases_from_pdf(user_story_input)

        print("📄 Generated BDD Test Cases from PDF:\n")
        print(result)

    except Exception as e:
        print(f"Error occurred: {e}")
