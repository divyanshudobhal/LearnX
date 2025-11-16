import json
import os

AI_LOG_FILE = "ai_logs.json"


def load_ai_logs():
    """Return list of all AI chatbot logs."""
    if not os.path.exists(AI_LOG_FILE):
        return []
    try:
        with open(AI_LOG_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_ai_logs(logs):
    with open(AI_LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)


def save_ai_log(question, answer, username):
    logs = load_ai_logs()
    logs.append({
        "user": username,
        "question": question,
        "answer": answer
    })
    save_ai_logs(logs)
