import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AI_LOGS_FILE = os.path.join(BASE_DIR, "ai_logs.json")


def load_ai_logs():
    if not os.path.exists(AI_LOGS_FILE):
        with open(AI_LOGS_FILE, "w") as f:
            json.dump([], f)
        return []
    try:
        with open(AI_LOGS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_ai_log(question, answer, user):
    logs = load_ai_logs()
    logs.append({
        "user": user,
        "question": question,
        "answer": answer
    })

    with open(AI_LOGS_FILE, "w") as f:
        json.dump(logs, f, indent=4)
