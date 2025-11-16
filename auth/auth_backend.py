import json
import os
import hashlib

# Base directory for JSON file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_DIR, "users.json")


# -----------------------------
# Load & Save Users
# -----------------------------
def load_users():
    """Load users safely from JSON."""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
        return {}

    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_users(users):
    """Save users to JSON."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


# -----------------------------
# Password Hashing
# -----------------------------
def hash_password(password):
    """Encrypt passwords using SHA-256 hashing."""
    return hashlib.sha256(password.encode()).hexdigest()


# -----------------------------
# Signup Logic
# -----------------------------
def signup_user(username, password, role):
    """Register a new user."""
    users = load_users()

    if username in users:
        return False, "❌ Username already exists!"

    users[username] = {
        "password": hash_password(password),
        "role": role
    }

    save_users(users)
    return True, f"✅ Signup successful! You are registered as {role}."


# -----------------------------
# Login Logic
# -----------------------------
def login_user(username, password):
    """Authenticate user credentials and return user object."""

    users = load_users()

    if username not in users:
        return False, "❌ User not found!", None

    stored_hash = users[username]["password"]
    if stored_hash != hash_password(password):
        return False, "⚠️ Incorrect password!", None

    # Return the full user object
    user_info = {
        "username": username,
        "role": users[username]["role"]
    }

    return True, "Login successful!", user_info
