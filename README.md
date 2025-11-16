# ☁️ E-Learning Platform (Cloud-Based)

A modern **cloud-enabled E-Learning Platform** built using **Python (CustomTkinter)** and **AWS S3**, allowing teachers to upload study materials directly to the cloud and students to browse, preview, and download them in real-time.

---

## 🚀 Features

### 👨‍🏫 Teacher Dashboard
- Upload **PDFs, images, videos, and text files** directly to **AWS S3**.
- Auto-generates **AI-based tags** for categorizing materials.
- View all uploaded files with timestamps and cloud URLs.

### 🎓 Student Dashboard
- Fetches file list **directly from AWS S3**.
- Search, filter, and preview files inline (PDF, images, text, videos).
- Download materials locally with one click.
- Integrated Chat Assistant (optional module).

### 🧑‍💼 Admin Dashboard
- Manage registered users and uploaded files.
- View statistics (total users, roles, uploaded files).
- Analyze platform usage in one place.

### 🔐 Authentication System
- Role-based signup and login system.
- Supports **Student**, **Teacher**, and **Admin** roles.
- Securely stores user data in `users.json`.

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| GUI | [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) |
| Cloud Storage | AWS S3 |
| Environment Management | python-dotenv |
| Backend | Python 3.11+ |
| JSON Storage | Local files (`users.json`, `uploads.json`) |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/e_learning_platform.git
cd e_learning_platform
