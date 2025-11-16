import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load API key from environment
api_key = os.getenv("GEMINI_API_KEY")

# Safety check
if not api_key:
    raise Exception("❌ Error: GEMINI_API_KEY is missing. Add it in Render environment variables.")

# Configure Gemini
genai.configure(api_key=api_key)

# Official working model
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_ai(question: str):
    if not question.strip():
        return "Please type a question."

    try:
        response = model.generate_content(question)
        return response.text.strip()
    except Exception as e:
        return f"AI Error: {e}"
