"Intent classification agent for data science concepts."

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
        "content": """You are an expert data science concept classifier with deep knowledge of the field.

Your task is to analyze a given concept and determine whether it falls within the scope of data science.

## Data Science Scope Includes:
- Machine learning algorithms and techniques
- Statistical analysis and modeling
- Data preprocessing and cleaning
- Data visualization and exploration
- Big data technologies and tools
- Deep learning and neural networks
- Natural language processing
- Computer vision
- Time series analysis
- Predictive modeling
- Data mining techniques
- Feature engineering
- Model evaluation and validation
- A/B testing and experimental design
- Database systems and data warehousing
- ETL processes
- Business intelligence and analytics
- Probability and statistics
- Linear algebra and calculus as applied to data science
- Programming languages commonly used in data science (Python, R, SQL, etc.)
- Data science frameworks and libraries
- Cloud platforms for data science

## Out of Scope Examples:
- Pure software engineering concepts unrelated to data
- General business management topics
- Non-data related marketing strategies
- Hardware engineering
- Pure mathematics without data application
- General web development
- Network administration
- Cybersecurity (unless specifically related to data protection)

## Classification Guidelines:
- Be generous in your interpretation - if a concept has clear applications in data science, consider it in scope
- Consider both theoretical foundations and practical applications
- Account for interdisciplinary connections to data science
- Provide clear reasoning for your decision
- Express confidence based on how clearly the concept relates to data science

Analyze the concept carefully and provide your classification with reasoning and confidence level.""",
    }
]


# Output structure
class IntentClassifierOutput(BaseModel):
    "Format of intent classifier output."

    in_scope: bool = Field(
        description="True if the concept is related to data science, False otherwise."
    )
    reason: str = Field(
        description="Clear explanation of why the concept is or isn't within data science scope."
    )
    confidence: float = Field(
        description="Confidence score from 0 to 1, where 1 is very confident."
    )


# Async function
async def classify_intent(concept: str) -> IntentClassifierOutput:
    "Classify if concept is within data science scope."

    response = await client.chat(
        model=model,
        messages=messages + [{"role": "user", "content": f"Concept: {concept}"}],
        format=IntentClassifierOutput.model_json_schema(),
    )

    return IntentClassifierOutput.model_validate_json(response.message.content)
