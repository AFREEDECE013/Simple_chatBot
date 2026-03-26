import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

# Configure API key
genai.configure(api_key=api_key)

# List all models
models = genai.list_models()

print("Available Models:\n")

for model in models:
    print(f"Name: {model.name}")
    print(f"Supported Methods: {model.supported_generation_methods}")
    print("-" * 50)