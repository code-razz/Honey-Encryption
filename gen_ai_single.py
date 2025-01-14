import os
import time
import re
from dotenv import load_dotenv
import google.generativeai as genai

# Suppress TensorFlow/absl log messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

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

# Function to handle retries
def generate_sentences_with_retry(model, prompt, retries=3):
    for attempt in range(retries):
        try:
            response = model.generate_content(prompt)
            raw_text = response.text.strip()

            # Debug: Print raw response for troubleshooting
            # print(f"Raw response:\n{raw_text}\n")

            # Adjust regex to extract the list (now more robust to multiple lines and edge cases)
            match = re.search(r"\[(.*?)\]", raw_text, re.DOTALL)
            if match:
                # Clean the result before passing to eval
                sentences_str = match.group(1).strip()
                sentences = eval(f"[{sentences_str}]")  # Wrap it with [] to ensure it's treated as a list

                # Check if the result is a valid list
                if isinstance(sentences, list):
                    return sentences
                else:
                    raise ValueError("Extracted content is not a valid list.")
            else:
                raise ValueError("No valid array found in the response.")
        except (SyntaxError, ValueError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Wait 2 seconds before retrying
    raise RuntimeError("All retry attempts failed.")

# Prompt to generate a Python array of sentences
prompt = "Give me an array of 10 random not commonly used single sentences, strictly in this format: ['sentence 1', 'sentence 2', ..., 'sentence 10']"

# Generate the sentences
try:
    sentences = generate_sentences_with_retry(model, prompt)
    print("Generated sentences stored in the array:")
    print(sentences)
except Exception as e:
    print(f"Failed to generate sentences: {e}")
