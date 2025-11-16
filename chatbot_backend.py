import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Correct Model Name
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_ai(question: str):
    if not question.strip():
        return "Please type a question."

    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"
