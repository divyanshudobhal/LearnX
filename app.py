from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
import json

# Backend helpers
from auth_backend import login_user, signup_user
from chatbot_backend import ask_ai
from utils.ai_tags import generate_ai_tags
from utils.storage_utils import upload_file_with_metadata, delete_file, rename_file
from utils.pdf_utils import summarize_pdf

load_dotenv()

# Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-key")


# ============================================
# 🔹 UPLOAD RECORD STORAGE HELPERS
# ============================================

UPLOAD_RECORD = "uploads.json"

def load_uploads():
    if not os.path.exists(UPLOAD_RECORD):
        return []
    with open(UPLOAD_RECORD, "r") as f:
        return json.load(f)

def save_uploads(data):
    with open(UPLOAD_RECORD, "w") as f:
        json.dump(data, f, indent=4)


# ============================================
# 🔹 LOGIN REQUIRED DECORATOR
# ============================================

def login_required(role=None):
    def wrapper(fn):
        def decorated(*args, **kwargs):
            if "username" not in session:
                return redirect(url_for("login"))
            if role and session.get("role") != role:
                return redirect(url_for("dashboard"))
            return fn(*args, **kwargs)
        decorated.__name__ = fn.__name__
        return decorated
    return wrapper


# ============================================
# 🔹 HOME + AUTH
# ============================================

@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        success, msg, user_info = login_user(username, password)
        if not success:
            return render_template("login.html", error=msg)

        session["username"] = username
        session["role"] = user_info["role"]
        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        r = request.form["role"]

        ok, msg = signup_user(u, p, r)
        if not ok:
            return render_template("signup.html", error=msg)

        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ============================================
# 🔹 DASHBOARD ROUTING LOGIC
# ============================================

@app.route("/dashboard")
@login_required()
def dashboard():
    role = session.get("role")

    if role == "Admin":
        return redirect(url_for("admin_dashboard"))
    if role == "Teacher":
        return redirect(url_for("teacher_dashboard"))
    return redirect(url_for("student_dashboard"))


@app.route("/dashboard/student")
@login_required("Student")
def student_dashboard():
    records = load_uploads()
    return render_template("student_dashboard.html",
                           username=session["username"],
                           files=records)


@app.route("/dashboard/teacher")
@login_required("Teacher")
def teacher_dashboard():
    return render_template("teacher_dashboard.html",
                           username=session["username"])


@app.route("/dashboard/admin")
@login_required("Admin")
def admin_dashboard():
    return render_template("admin_dashboard.html",
                           username=session["username"])


# ============================================
# 🔹 CHATBOT
# ============================================

@app.route("/chatbot", methods=["GET"])
@login_required()
def chatbot():
    return render_template("chatbot.html")


@app.post("/api/chat")
@login_required()
def api_chat():
    data = request.get_json()
    question = data.get("message", "")
    answer = ask_ai(question)
    return {"answer": answer}


# ============================================
# 🔹 FILE UPLOAD (Teacher)
# ============================================

@app.route("/upload", methods=["GET", "POST"])
@login_required("Teacher")
def upload_page():
    if request.method == "POST":
        file = request.files.get("file")

        if not file:
            return render_template("upload.html", error="Please choose a file.")

        filename = secure_filename(file.filename)

        # Temporary save before uploading to S3
        temp_folder = "uploads"
        os.makedirs(temp_folder, exist_ok=True)
        temp_path = os.path.join(temp_folder, filename)
        file.save(temp_path)

        # Upload to S3 → CloudFront URL
        s3_url = upload_file_with_metadata(temp_path, key=filename)

        # AI tags
        tags = generate_ai_tags(filename)

        # AI Summary (PDF)
        summary = None
        if filename.lower().endswith(".pdf"):
            summary = summarize_pdf(temp_path)

        # Save metadata
        records = load_uploads()
        records.append({
            "uploaded_by": session["username"],
            "filename": filename,
            "url": s3_url,
            "tags": tags,
            "summary": summary
        })
        save_uploads(records)

        os.remove(temp_path)

        return render_template("upload_success.html",
                               url=s3_url, tags=tags)

    return render_template("upload.html")


# ============================================
# 🔹 VIEW ALL FILES (Students + Admin)
# ============================================

@app.route("/files")
@login_required()
def files_page():
    records = load_uploads()
    return render_template("files.html", files=records)


# ============================================
# 🔹 TEACHER FILE MANAGER
# ============================================

@app.route("/teacher/files")
@login_required("Teacher")
def teacher_files():
    all_records = load_uploads()
    mine = [r for r in all_records if r.get("uploaded_by") == session["username"]]
    return render_template("teacher_files.html", files=mine)


@app.post("/teacher/files/delete/<filename>")
@login_required("Teacher")
def delete_teacher_file(filename):
    records = load_uploads()
    new_records = []
    to_delete = None

    for r in records:
        if r["filename"] == filename and r.get("uploaded_by") == session["username"]:
            to_delete = r
            continue
        new_records.append(r)

    if to_delete:
        try:
            delete_file(to_delete["filename"])
        except Exception as e:
            print("Delete Error:", e)

        save_uploads(new_records)

    return redirect(url_for("teacher_files"))


@app.post("/teacher/files/rename/<filename>")
@login_required("Teacher")
def rename_teacher_file(filename):
    new_name = request.form.get("new_name", "").strip()
    if not new_name:
        return redirect(url_for("teacher_files"))

    records = load_uploads()
    for r in records:
        if r["filename"] == filename and r.get("uploaded_by") == session["username"]:

            # Rename in S3
            try:
                rename_file(filename, new_name)
            except Exception as e:
                print("Rename Error:", e)
                return redirect(url_for("teacher_files"))

            r["filename"] = new_name
            r["url"] = upload_file_with_metadata("uploads/" + new_name, key=new_name)
            r["tags"] = generate_ai_tags(new_name)

            break

    save_uploads(records)
    return redirect(url_for("teacher_files"))


# ============================================
# 🔹 MAIN ENTRY
# ============================================

if __name__ == "__main__":
    app.run(debug=True)
