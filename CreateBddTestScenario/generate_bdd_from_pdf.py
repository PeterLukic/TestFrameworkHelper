# file: generate_bdd_from_pdf.py

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import UnstructuredPDFLoader

# Initialize LLMs
qwen_llm = ChatOllama(
    model="qwen2.5", 
    base_url="http://localhost:11434", 
    temperature=0.5
)

embedding_llm  = ChatOllama(
    model="embeddinggemma", 
    base_url="http://localhost:11434", 
    temperature=0.5
)

llama_llm = ChatOllama(
    model="llama3.2:latest",        
    base_url="http://localhost:11434",
    temperature=0.5
)

gemma312_llm = ChatOllama(
    model="gemma3:12b",        
    base_url="http://localhost:11434",
    temperature=0.5
)


deepseekcloud_llm = ChatOllama(
    model="deepseek-v3.1:671b-cloud",        
    base_url="http://localhost:11434",
    temperature=0.5
)


def generate_bdd_test_cases_from_pdf(user_story: str) -> str:
    """
    📄 Reads requirements from a specific PDF file and generates comprehensive 
    BDD test scenarios in Gherkin format.
    Includes valid, invalid, edge case, and alternative flows.
    """
    pdf_file = "./Docs/LoginDocumentation.pdf"
    loader = UnstructuredPDFLoader(
        file_path=pdf_file,
        languages=["eng"]  # preferred parameter for OCR
    )
    docs = loader.load()

    requirements_text = "\n\n".join([doc.page_content.strip() for doc in docs])[:2000]

    prompt_template = PromptTemplate.from_template(
        """
        You are a QA Automation Engineer. 
        Your task is to convert the following user story into ALL possible test cases 
        in Gherkin BDD style format.
        Include valid, invalid, edge case, and alternative flow scenarios.

        {requirements_text}

        Format your response as:
        Feature: [Feature name]

        Scenario: [Scenario name]
            Given [precondition]
            When [action]
            Then [expected result]
        """
    )

    prompt = prompt_template.format(requirements_text=requirements_text)
    response = gemma312_llm.invoke(prompt)

    if hasattr(response, 'content'):
        return response.content
    else:
        return str(response)


def generate_single_bdd_test_case_from_pdf(user_story: str) -> str:
    """
    📄 Reads requirements from a specific PDF file and generates a single 
    BDD test scenario in Gherkin format.
    Includes a combination of valid, invalid, edge case, or alternative flows.
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
        You are a QA Automation Engineer. 
        Your task is to convert the following user story into ONLY ONE test case 
        in Gherkin BDD style format. 

        {requirements_text}

        Format your response as:
        Feature: [Feature name]

        Scenario: [Scenario name]
            Given [precondition]
            When [action]
            Then [expected result]
        """
    )

    prompt = prompt_template.format(requirements_text=requirements_text)
    response = deepseekcloud_llm.invoke(prompt)

    if hasattr(response, 'content'):
        return response.content
    else:
        return str(response)


if __name__ == "__main__":
    # Input for the tool
    user_story_input = "Generate BDD test cases from PDF"

    # Directly call the tool
    try:
        #result = generate_single_bdd_test_case_from_pdf(user_story_input)
        result = generate_bdd_test_cases_from_pdf(user_story_input)
        print("📄 Generated BDD Test Cases from PDF:\n")
        print(result)
    except Exception as e:
        print(f"Error occurred: {e}")
