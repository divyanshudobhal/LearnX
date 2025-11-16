import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load your API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Correct model path for v1beta API
MODEL_NAME = "models/gemini-1.5-flash"

model = genai.GenerativeModel(MODEL_NAME)

def ask_ai(question: str):
    if not question.strip():
        return "Please type a question."

    try:
        response = model.generate_content(question)
        return response.text.strip()
    except Exception as e:
        return f"AI Error: {e}"
