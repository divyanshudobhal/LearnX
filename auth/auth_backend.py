import json
import os
import hashlib

# -------------------------------------------------
# FIXED PATH – Works on both Local & Render
# -------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
USERS_FILE = os.path.join(BASE_DIR, "users.json")


# -------------------------------------------------
# LOAD USERS
# -------------------------------------------------
def load_users():
    """Load user data from users.json."""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
        return {}

    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


# -------------------------------------------------
# SAVE USERS
# -------------------------------------------------
def save_users(users):
    """Write user data to users.json."""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)


# -------------------------------------------------
# HASH PASSWORD
# -------------------------------------------------
def hash_password(password):
    """Encrypt password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


# -------------------------------------------------
# SIGNUP USER
# -------------------------------------------------
def signup_user(username, password, role):
    """Create a new user."""
    users = load_users()

    if username in users:
        return False, "❌ Username already exists!"

    users[username] = {
        "password": hash_password(password),
        "role": role
    }

    save_users(users)
    return True, f"✅ Signup successful! Registered as {role}."


# -------------------------------------------------
# LOGIN USER
# -------------------------------------------------
def login_user(username, password):
    """Validate user credentials."""
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
