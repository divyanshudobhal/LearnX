import json
import os
import hashlib

# ============================================
# Correct JSON Path Handling (Works on Render)
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "..", "users.json")
USERS_FILE = os.path.abspath(USERS_FILE)


# ============================================
# Load & Save Users
# ============================================
def load_users():
    """Load users safely from JSON as a dict."""
    
    # If file missing → create with DEFAULT admin
    if not os.path.exists(USERS_FILE):
        default_data = {
            "admin": {
                "password": hash_password("admin123"),
                "role": "Admin"
            }
        }
        save_users(default_data)
        return default_data

    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)

            # If file is empty → restore default admin
            if not isinstance(data, dict) or len(data) == 0:
                default_data = {
                    "admin": {
                        "password": hash_password("admin123"),
                        "role": "Admin"
                    }
                }
                save_users(default_data)
                return default_data

            return data

    except json.JSONDecodeError:
        # File corrupted → recreate with default admin
        default_data = {
            "admin": {
                "password": hash_password("admin123"),
                "role": "Admin"
            }
        }
        save_users(default_data)
        return default_data


def save_users(users):
    """Save users to JSON."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


# ============================================
# Password Hashing
# ============================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ============================================
# Signup Logic
# ============================================
def signup_user(username, password, role):
    users = load_users()

    if username in users:
        return False, "❌ Username already exists!"

    users[username] = {
        "password": hash_password(password),
        "role": role
    }
    
    save_users(users)
    return True, f"✅ Signup successful! Registered as {role}."


# ============================================
# Login Logic
# ============================================
def login_user(username, password):
    users = load_users()

    if username not in users:
        return False, "❌ User not found!", None

    stored_hash = users[username]["password"]
    if stored_hash != hash_password(password):
        return False, "⚠️ Incorrect password!", None

    return True, "Login successful!", {
        "username": username,
        "role": users[username]["role"]
    }
