import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Load key (safe)
genai.configure(api_key=os.getenv("AIzaSyD952mhQGB06f6GEJKU5ayuB1y3ek_8SxI"))

# 🟢 WORKING MODEL (official)
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_ai(question: str):
    if not question.strip():
        return "Please type a question."

    try:
        response = model.generate_content(question)
        return response.text.strip()
    except Exception as e:
        return f"AI Error: {e}"
