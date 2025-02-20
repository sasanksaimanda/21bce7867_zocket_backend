# Task Management System

This is a **Flask-based Task Management System** with authentication, real-time task handling, AI-powered suggestions, and deployment on **Render**.

## Features
✅ JWT-based Authentication (Register/Login)
✅ CRUD Operations on Tasks
✅ AI-Powered Task Suggestions (Google Gemini API)
✅ MongoDB as Database (MongoDB Atlas)
✅ Deployment on Render

---
## 1️⃣ Setup & Installation

### **Prerequisites**
- Python 3.12 installed
- MongoDB Atlas account (or local MongoDB)
- OpenAI API key (if using GPT-based AI) or Google Gemini API key
- GitHub account (for deployment)

### **Clone the Repository**
```sh
 git clone <repo-url>
 cd task-management
```

### **Create a Virtual Environment**
```sh
 python -m venv venv
 source venv/bin/activate  # For Linux/macOS
 venv\Scripts\activate     # For Windows
```

### **Install Dependencies**
```sh
 pip install -r requirements.txt
```

### **Set Up Environment Variables**
Create a `.env` file in the project root and add:
```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/zocket
JWT_SECRET_KEY=<your-secret-key>
GEMINI_API_KEY=<your-gemini-api-key>
```

---
## 2️⃣ Run the Application Locally

```sh
 flask run --host=0.0.0.0 --port=5000
```

**API Base URL:** `http://127.0.0.1:5000`

---
## 3️⃣ API Endpoints

### **Authentication Routes** (`auth.py`)
- **Register:** `POST /auth/register`
- **Login:** `POST /auth/login`
- **Protected Route:** `GET /auth/protected`

### **Task Management Routes** (`tasks.py`)
- **Create Task:** `POST /tasks/create`
- **Get All Tasks:** `GET /tasks/`
- **Get Single Task:** `GET /tasks/<task_id>`
- **Update Task:** `PUT /tasks/update/<task_id>`
- **Delete Task:** `DELETE /tasks/delete/<task_id>`

### **AI Suggestions** (`ai_suggestions.py`)
- **Suggest Tasks:** `POST /ai/suggest`

**Example Request:**
```json
{
  "query": "Suggest tasks for software developers"
}
```

---
## 4️⃣ Deployment on Render

### **1. Push to GitHub**
```sh
git add .
git commit -m "Initial commit"
git push origin main
```

### **2. Create a Render Web Service**
- Go to [Render](https://render.com)
- Click **New Web Service**
- Connect your GitHub repo
- Set **Build Command**: `pip install -r requirements.txt`
- Set **Start Command**: `gunicorn app:app`
- Add environment variables from `.env` file
- Click **Deploy**

### **3. Add a `Procfile` (Required for Render)**
Create a file named `Procfile` in the project root with:
```sh
web: gunicorn app:app
```

### **4. Access Your Application**
Once deployed, Render will provide a live URL (e.g., `https://your-app.onrender.com`).

---
## 5️⃣ Possible Issues & Fixes

### **Error: `Missing claim: sub` in JWT**
✔️ Ensure `sub` (email) is included when generating JWT tokens in `auth.py`:
```python
jwt.encode({"sub": user["email"], "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, JWT_SECRET_KEY, algorithm="HS256")
```

### **Error: `ModuleNotFoundError: No module named 'google'`**
✔️ Install Google Gemini API package:
```sh
pip install google-generativeai
```

### **Error: `You exceeded your current quota` (Gemini API)**
✔️ Check API usage at [Google AI Console](https://ai.google.dev)

---
## 🎯 Future Enhancements
✅ WebSocket for Real-Time Updates
✅ Notifications & Email Alerts
✅ Advanced AI-powered Task Management
✅ CI/CD Pipeline for Automated Deployment

---
## 📢 Contributions
Contributions are welcome! Feel free to submit issues or pull requests.

---
## 📞 Contact
For any queries, reach out to **Sasank Sai Manda** at `sasankmanda8@gmail.com`.

🚀 **Happy Coding!**

