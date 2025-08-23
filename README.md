# 🎥 Videoflix

> **Videoflix** is your own Netflix-style streaming platform: user management, video upload, email activation, Docker-based deployment – ready to launch!

---

## 🚀 Features

- 🔑 User registration & login with activation email  
- 🔒 Password reset via email  
- 👥 Roles & permissions (User / Admin)  
- 📂 Upload & manage videos / content  
- 🗂️ PostgreSQL as database, Redis for caching/queues  
- 🐳 Deployment with Docker & Docker Compose  
- ⚡ HLS streaming (video manifest & segments)  

---

## 🛠 Technologies & Architecture

- **Backend:** Django + Django REST Framework  
- **Auth:** JWT cookies with email activation & reset  
- **DB:** PostgreSQL  
- **Caching/Queue:** Redis  
- **Deployment:** Docker & Docker Compose  
- **Configuration:** `.env` based configuration  

**Architecture:**

```
[Frontend] ↔ [Django Backend API] ↔ [PostgreSQL]
                             ↘ [Redis Cache/Queue]
```

---

## 📂 Project Structure

```text
videoflix/
├── auth_app/             # Authentication & email templates
├── content_app/          # Video & media management
├── core/                 # Settings, URLs, WSGI / ASGI
├── media/                # Uploaded videos
├── static/               # Static assets
├── docker-compose.yml
├── backend.Dockerfile
├── requirements.txt
└── manage.py
```

---

## ⚙️ Installation & Setup

### Requirements
- Python **3.12+**  
- Docker & Docker Compose  
- (Optional) Virtualenv  

### Local Setup (without Docker)
```bash
# Clone repo
git clone https://github.com/your-user/videoflix.git
cd videoflix

# Virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.template .env

# Run migrations & create superuser
python manage.py migrate
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### With Docker
```bash
docker compose up --build

# Stop
docker compose down
```

---

## 🔑 Environment Variables

Example (`.env.template`):

```ini
# Superuser
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=adminpassword
DJANGO_SUPERUSER_EMAIL=admin@example.com

# Django Framework
SECRET_KEY="django-insecure-***"
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:4200,http://127.0.0.1:4200

# Database (Postgres)
DB_NAME=videoflix_db
DB_USER=videoflix_user
DB_PASSWORD=videoflix_pass
DB_HOST=db
DB_PORT=5432

# Redis Cache / Queue
REDIS_HOST=redis
REDIS_LOCATION=redis://redis:6379/1
REDIS_PORT=6379
REDIS_DB=0

# SMTP Configuration
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email_user
EMAIL_HOST_PASSWORD=your_email_user_password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=default_from_email
```

---

## 📡 API (Quick Reference)

### 🔐 Authentication & Users

`POST /api/register/`  
➡️ Register a new account  

`POST /api/login/`  
➡️ Login with email/password (JWT cookie)  

`POST /api/logout/`  
➡️ Logout, token invalidated  

`GET /api/activate/<uidb64>/<token>/`  
➡️ Activate a user account after email verification  

`POST /api/token/refresh/`  
➡️ Refresh the JWT cookie  

`POST /api/password_reset/`  
➡️ Send reset email  

`POST /api/password_reset/confirm/<uidb64>/<token>/`  
➡️ Set a new password  

---

### 🎬 Video & Streaming

`GET /api/video/`  
➡️ List all videos  

`GET /api/video/<movie_id>/<resolution>/index.m3u8`  
➡️ Manifest for HLS streaming (e.g., 480p, 720p, 1080p)  

`GET /api/video/<movie_id>/<resolution>/<segment>/`  
➡️ Fetch a specific HLS segment  

---

## 📈 Roadmap

- [ ] Video streaming with FFmpeg transcoding  

---

## 👨‍💻 Author

- **Name:** Özgür Taylan Umucu  
- **Portfolio:** [oezguer-taylan.umucu.de](https://oezguer-taylan.umucu.de/)  
- **LinkedIn:** [linkedin.com/in/taylan-umucu-83132325b](https://www.linkedin.com/in/taylan-umucu-83132325b)
