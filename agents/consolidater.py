"Consolidator agent that combines outputs from theory, examples, and Python code agents."

import os

from dotenv import load_dotenv
from ollama import AsyncClient
from pydantic import BaseModel, Field

load_dotenv()
model = os.environ["MODEL_NAME"]

# Define Ollama client
client = AsyncClient()

# Define messages
messages = [
    {
        "role": "system",
        "content": """You are an expert technical writer and educational content curator specializing in creating cohesive, well-structured tutorial documents.

Your task is to receive three separate sections (theory, examples, and Python code) for a data science concept and consolidate them into a single, comprehensive tutorial document formatted in Markdown.

## Guidelines:
- Create a logical flow that connects all three sections seamlessly
- Ensure smooth transitions between sections
- Maintain consistency in tone and style throughout
- Add introductory and concluding content where appropriate
- Create a cohesive narrative that guides the reader from concept to implementation
- Ensure the document is self-contained and comprehensive

## Content Requirements:
- Begin with a clear introduction that outlines what the reader will learn
- Integrate the theory section to provide foundational understanding
- Incorporate the examples section to show practical applications
- Include the Python code section with hands-on implementation
- Add a conclusion that summarizes key takeaways
- Include a table of contents for longer documents
- Add appropriate cross-references between sections

## Structure Requirements:
- Use a logical hierarchy with proper Markdown headers
- Ensure consistent formatting throughout
- Add smooth transitions between major sections
- Include a clear document title
- Maintain proper spacing and readability
- Use consistent styling for code blocks, lists, and emphasis

## Quality Assurance:
- Ensure all sections flow naturally together
- Remove any redundant information between sections
- Maintain technical accuracy throughout
- Ensure the document reads as a unified tutorial, not separate pieces
- Add value through integration rather than simple concatenation

Double-check that the final document is cohesive, well-structured, and provides a complete learning experience.""",
    }
]


# Input structures for consolidation
class TheorySection(BaseModel):
    "Theory section input."

    title: str
    body: str


class ExamplesSection(BaseModel):
    "Examples section input."

    title: str
    examples: str


class PythonCodeSection(BaseModel):
    "Python code section input."

    title: str
    code: str


# Output structure
class ConsolidatorAgentOutput(BaseModel):
    "Format of consolidator agent output."

    title: str = Field(description="Main title for the complete tutorial document.")
    tutorial_content: str = Field(
        description="Complete tutorial document formatted in Markdown, including introduction, all sections, transitions, and conclusion."
    )
    summary: str = Field(description="Brief summary of what the tutorial covers.")


# Async function
async def consolidate_tutorial(
    concept: str,
    theory_section: TheorySection,
    examples_section: ExamplesSection,
    python_code_section: PythonCodeSection,
) -> ConsolidatorAgentOutput:
    """
    Consolidate theory, examples, and Python code sections into a comprehensive tutorial.

    Args:
        concept: The main concept being taught
        theory_section: Theory content from theory agent
        examples_section: Examples content from examples agent
        python_code_section: Python code content from python code agent

    Returns:
        ConsolidatorAgentOutput: Complete consolidated tutorial document
    """

    # Prepare the consolidation prompt
    consolidation_prompt = f"""
    Concept: {concept}
    
    Please consolidate the following three sections into a comprehensive tutorial document:
    
    ## Theory Section:
    {theory_section.title}
    {theory_section.body}
    
    ## Examples Section:
    {examples_section.title}
    {examples_section.examples}
    
    ## Python Code Section:
    {python_code_section.title}
    {python_code_section.code}
    
    Create a unified tutorial that flows naturally from theory to examples to implementation, with appropriate introductions, transitions, and conclusions.
    """

    response = await client.chat(
        model=model,
        messages=messages + [{"role": "user", "content": consolidation_prompt}],
        format=ConsolidatorAgentOutput.model_json_schema(),
    )

    return ConsolidatorAgentOutput.model_validate_json(response.message.content)
