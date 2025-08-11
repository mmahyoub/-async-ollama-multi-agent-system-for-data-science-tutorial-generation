"""
Pull the open-source model from the Ollama hub
"""

import os
import subprocess

from dotenv import load_dotenv

load_dotenv()

model = os.environ["MODEL_NAME"]


def pull_model(model_name: str):
    try:
        subprocess.run(["ollama", "pull", model_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error pulling model: {e.stderr}")


if __name__ == "__main__":
    pull_model(model)
