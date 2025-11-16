import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Correct way: load API_KEY from environment variable
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini safely
genai.configure(api_key=api_key)

# Use official model name
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_ai(question: str):
    if not question.strip():
        return "Please type a question."

    try:
        response = model.generate_content(question)
        return response.text.strip()
    except Exception as e:
        return f"AI Error: {e}"
