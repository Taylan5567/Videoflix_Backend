# 🎥 Videoflix

> **Videoflix** ist deine eigene Streaming-Plattform im Stil von Netflix: Benutzerverwaltung, Video-Upload, E-Mail-Aktivierung, Docker-basiertes Deployment – alles ready, um produktiv zu starten!

---

## 🚀 Features

- 🔑 Benutzerregistrierung & Login mit Aktivierungs-E-Mail  
- 🔒 Passwort-Zurücksetzen via E-Mail  
- 👥 Rollen & Berechtigungen (User / Admin)  
- 📂 Upload & Verwaltung von Videos / Inhalten  
- 🗂️ PostgreSQL als Datenbank, Redis für Caching/Queues  
- 🐳 Deployment mit Docker & Docker Compose  
- ⚡ HLS-Streaming (Video Manifest & Segmente)  

---

## 🛠 Technologien & Architektur

- **Backend:** Django + Django REST Framework  
- **Auth:** JWT-Cookies mit E-Mail-Aktivierung & Reset  
- **DB:** PostgreSQL  
- **Caching/Queue:** Redis  
- **Deployment:** Docker & Docker Compose  
- **Konfiguration:** `.env` basierte Konfiguration  

**Architektur:**

```
[Frontend] ↔ [Django Backend API] ↔ [PostgreSQL]
                             ↘ [Redis Cache/Queue]
```

---

## 📂 Projektstruktur

```text
videoflix/
├── auth_app/             # Authentifizierung & E-Mail-Templates
├── content_app/          # Videos & Medienverwaltung
├── core/                 # Settings, URLs, WSGI / ASGI
├── media/                # Hochgeladene Videos
├── static/               # Statische Assets
├── docker-compose.yml
├── backend.Dockerfile
├── requirements.txt
└── manage.py
```

---

## ⚙️ Installation & Setup

### Voraussetzungen
- Python **3.12+**  
- Docker & Docker Compose  
- (Optional) Virtualenv  

### Lokales Setup (ohne Docker)
```bash
# Repo klonen
git clone https://github.com/dein-user/videoflix.git
cd videoflix

# Virtuelle Umgebung
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# .env anlegen
cp .env.template .env

# Migrationen anwenden & Superuser erstellen
python manage.py migrate
python manage.py createsuperuser

# Server starten
python manage.py runserver
```

### Mit Docker
```bash
docker compose up --build

# Stoppen
docker compose down
```

---

## 🔑 Umgebungsvariablen

Beispiel (`.env.template`):

```ini
# Superuser
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=adminpassword
DJANGO_SUPERUSER_EMAIL=admin@example.com

# Django Framework
SECRET_KEY="django-insecure-***"
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500

# Datenbank (Postgres)
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

# SMTP Konfiguration
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email_user
EMAIL_HOST_PASSWORD=your_email_user_password
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=default_from_email
```

---

## 📡 API (Kurzreferenz)

### 🔐 Authentifizierung & Benutzer

`POST /api/register/`  
➡️ Neues Konto registrieren  

`POST /api/login/`  
➡️ Login mit E-Mail/Passwort (JWT Cookie)  

`POST /api/logout/`  
➡️ Logout, Token wird invalidiert  

`GET /api/activate/<uidb64>/<token>/`  
➡️ Aktiviert ein Benutzerkonto nach E-Mail-Verifikation  

`POST /api/token/refresh/`  
➡️ Frischt das JWT Cookie auf  

`POST /api/password_reset/`  
➡️ Sendet eine E-Mail mit Reset-Link  

`POST /api/password_reset/confirm/<uidb64>/<token>/`  
➡️ Setzt ein neues Passwort  

---

### 🎬 Video & Streaming

`GET /api/video/`  
➡️ Liste aller Videos  

`GET /api/video/<movie_id>/<resolution>/index.m3u8`  
➡️ Manifest für HLS-Streaming (z. B. 480p, 720p, 1080p)  

`GET /api/video/<movie_id>/<resolution>/<segment>/`  
➡️ Holt ein spezifisches HLS-Segment  

---

---

## 🧪 Tests

```bash
python manage.py test
```

---

## 📈 Roadmap

- [ ] Video-Streaming mit FFmpeg-Transcoding  
- [ ] Playlists & Favoriten  
- [ ] Mehrsprachigkeit (Deutsch / Englisch / Türkisch)  
- [ ] Abo-Modell mit Zahlungsintegration  
- [ ] Admin-Dashboard mit Statistiken & Analytics  

---

## 👨‍💻 Autor

- **Name:** Özgür Taylan Umucu  
- **Portfolio:** [oezguer-taylan.umucu.de](https://oezguer-taylan.umucu.de/)  
- **LinkedIn:** [linkedin.com/in/taylan-umucu-83132325b](https://www.linkedin.com/in/taylan-umucu-83132325b)
