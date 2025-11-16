import json
import os

AI_LOGS_FILE = "ai_logs.json"

def load_ai_logs():
    if not os.path.exists(AI_LOGS_FILE):
        with open(AI_LOGS_FILE, "w") as f:
            json.dump([], f)
        return []
    with open(AI_LOGS_FILE, "r") as f:
        return json.load(f)

def save_ai_log(question, answer, user):
    logs = load_ai_logs()
    logs.append({
        "user": user,
        "question": question,
        "answer": answer
    })
    with open(AI_LOGS_FILE, "w") as f:
        json.dump(logs, f, indent=4)
