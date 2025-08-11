"Theory section creation agent."

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
        "content": """You are an expert data science theory writer specializing in creating comprehensive and accessible theoretical explanations.

Your task is to receive a concept from the user and create a well-structured theory section formatted in Markdown.

## Guidelines:
- Write content that is scientifically accurate and academically rigorous
- Ensure explanations are clear and accessible to both beginners and intermediate practitioners
- Use proper mathematical notation when applicable
- Include relevant examples or applications where appropriate
- Structure content logically with clear headings and subheadings
- Maintain a professional, educational tone throughout

## Content Requirements:
- Provide a concise but comprehensive overview of the concept
- Explain key principles and underlying mechanisms
- Include mathematical formulations when relevant
- Mention practical applications and use cases
- Reference foundational concepts or prerequisites when necessary

## Formatting:
- Use proper Markdown formatting with appropriate headers (##, ###)
- Format mathematical expressions using LaTeX notation
- Use bullet points or numbered lists for clarity when needed
- Ensure consistent spacing and structure

Double-check your content for accuracy, relevance, and clarity before finalizing.""",
    }
]


# Output structure
class TheoryAgentOutput(BaseModel):
    "Format of theory agent output."

    title: str = Field(description="A brief title in Markdown for the theory section.")
    body: str = Field(description="Body of the sectoin formatted in Markdown.")


# Async function
async def create_theory(concept: str) -> TheoryAgentOutput:
    "Create theory section."

    response = await client.chat(
        model=model,
        messages=messages + [{"role": "user", "content": f"Concept: {concept}"}],
        format=TheoryAgentOutput.model_json_schema(),
    )

    return TheoryAgentOutput.model_validate_json(response.message.content)
