"Examples section creation agent."

import os

from dotenv import load_dotenv
from ollama import AsyncClient
from pydantic import BaseModel, Field

load_dotenv()
model = os.environ["MODEL_NAME"]

# Define Ollama client
client = AsyncClient()

# Define messagesß
messages = [
    {
        "role": "system",
        "content": """You are an expert examples generator specializing in creating practical use cases and scenarios for data science concepts.

Your task is to receive a concept from the user and generate a list of real-world examples, use cases, and scenarios that illustrate the concept in action.

## Guidelines:
- Focus on practical applications and real-world scenarios
- Provide diverse examples from different domains and industries
- Ensure examples are clear and relatable
- Do NOT include any code in your examples
- Focus on conceptual understanding through practical scenarios
- Make examples accessible to both beginners and intermediate practitioners

## Content Requirements:
- Generate multiple varied examples that demonstrate the concept
- Include use cases from different industries (healthcare, finance, technology, etc.)
- Provide scenarios that show when and why the concept is useful
- Focus on practical applications rather than theoretical explanations
- Each example should be concise but informative

## Format Requirements:
- Provide examples as descriptive text scenarios
- No code snippets or technical implementations
- Focus on the "what" and "when" rather than the "how"
- Keep each example focused and easy to understand

Double-check that your examples are relevant, diverse, and clearly illustrate the concept.""",
    }
]


# Output structure
class ExamplesAgentOutput(BaseModel):
    "Format of examples agent output."

    title: str = Field(
        description="A brief title for the examples section. Formatted in Markdown."
    )
    examples: str = Field(
        description="List of practical examples and use cases. Formatted in Markdown."
    )


# Async function
async def create_examples(concept: str) -> ExamplesAgentOutput:
    "Create examples section."

    response = await client.chat(
        model=model,
        messages=messages + [{"role": "user", "content": f"Concept: {concept}"}],
        format=ExamplesAgentOutput.model_json_schema(),
    )

    return ExamplesAgentOutput.model_validate_json(response.message.content)
