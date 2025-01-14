import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Get the API key from the .env file
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set GEMINI_API_KEY in your .env file.")

# Configure the API
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

# List to store responses
responses = []

# Generate content 10 times and store each response
for _ in range(10):
    response = model.generate_content("Give me just a single totally random sentence")
    responses.append(response.text)

# Print all responses
for idx, text in enumerate(responses, start=1):
    print(f"{text}")
