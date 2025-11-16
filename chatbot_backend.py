import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# UNIVERSAL MODEL (works on Render + all API versions)
MODEL_NAME = "models/gemini-1.0-pro"

model = genai.GenerativeModel(MODEL_NAME)

def ask_ai(question: str):
    if not question.strip():
        return "Please type a question."

    try:
        response = model.generate_content(question)
        return response.text.strip()
    except Exception as e:
        return f"AI Error: {e}"

