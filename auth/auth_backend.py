import hashlib
from database import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(username, password, role):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT username FROM users WHERE username=?", (username,))
    if cur.fetchone():
        return False, "Username already exists!"

    cur.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, hash_password(password), role)
    )
    conn.commit()
    conn.close()

    return True, "Signup successful!"

def login_user(username, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT username, password, role FROM users WHERE username=?", (username,))
    row = cur.fetchone()

    if not row:
        return False, "User not found!", None

    if row[1] != hash_password(password):
        return False, "Incorrect password!", None

    conn.close()
    return True, "Login successful!", {"username": row[0], "role": row[2]}

def load_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT username, role FROM users")
    rows = cur.fetchall()
    conn.close()

    return [{"username": r[0], "role": r[1]} for r in rows]
