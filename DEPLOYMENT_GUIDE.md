# 🚀 Complete Deployment Guide: Django Portfolio on Render & GitHub

This guide walks you through deploying your full-stack Django 3D Portfolio to **GitHub** and **Render** with PostgreSQL database, WhiteNoise static files, AI Chatbot integration, and media handling.

---

## 📋 Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Step 1: Push Code to GitHub](#2-step-1-push-code-to-github)
3. [Step 2: Deploy on Render](#3-step-2-deploy-on-render)
   - [Method A: Automatic Blueprint Deploy (Fastest)](#method-a-automatic-blueprint-deploy-fastest)
   - [Method B: Manual Web Service + PostgreSQL Setup](#method-b-manual-web-service--postgresql-setup)
4. [Step 3: Environment Variables Reference](#4-step-3-environment-variables-reference)
5. [Step 4: Create Django Admin Superuser on Render](#5-step-4-create-django-admin-superuser-on-render)
6. [Step 5: Verify Your Live Portfolio](#6-step-5-verify-your-live-portfolio)
7. [Optional: Keep Render Free Tier Active (No Cold Starts)](#7-optional-keep-render-free-tier-active-no-cold-starts)
8. [Troubleshooting & Common Questions](#8-troubleshooting--common-questions)

---

## 1. Prerequisites

Before starting, ensure you have:
1. A **[GitHub](https://github.com/)** account.
2. A **[Render](https://render.com/)** account (you can sign in with GitHub).
3. Your **OpenRouter API Key** (for the AI chatbot).

---

## 2. Step 1: Push Code to GitHub

### 2.1 Create a New GitHub Repository
1. Go to [GitHub New Repository](https://github.com/new).
2. Set **Repository name** (e.g., `portfolio` or `django-3d-portfolio`).
3. Set Visibility to **Public** or **Private**.
4. **Do NOT** check "Add a README", ".gitignore", or "license" (we already created them locally).
5. Click **Create repository**.

### 2.2 Push Local Project to GitHub
In your local project terminal (PowerShell or Git Bash), run:

```bash
# 1. Add all files to git
git add .

# 2. Make your initial commit
git commit -m "Initial commit: Production-ready Django portfolio for Render"

# 3. Rename branch to main
git branch -M main

# 4. Link your remote GitHub repository (replace with your repo URL)
git remote add origin https://github.com/NagasrinivasGovvala/YOUR_REPOSITORY_NAME.git

# 5. Push to GitHub
git push -u origin main
```

---

## 3. Step 2: Deploy on Render

You can deploy using either **Method A (Blueprint)** or **Method B (Manual Dashboard)**.

---

### Method A: Automatic Blueprint Deploy (Fastest)

Render includes a `render.yaml` file in this repository which sets up both the Web Service and PostgreSQL database automatically.

1. Go to your **[Render Dashboard](https://dashboard.render.com/)**.
2. Click **New +** (top right) $\rightarrow$ **Blueprint**.
3. Connect your GitHub account and select your portfolio repository.
4. Render will detect `render.yaml`.
5. Enter any required environment variables (such as `OPENROUTER_API_KEY`).
6. Click **Apply**.
7. Render will automatically provision PostgreSQL, run `build.sh`, and start your web service!

---

### Method B: Manual Web Service + PostgreSQL Setup

If you prefer to configure services manually from the dashboard:

#### 1. Create a PostgreSQL Database on Render
1. Click **New +** $\rightarrow$ **PostgreSQL**.
2. Fill in:
   - **Name**: `portfolio-db`
   - **Database**: `portfolio_db`
   - **User**: `portfolio_user`
   - **Region**: Choose closest to you (e.g., `Singapore`, `Frankfurt`, or `Oregon`)
   - **Plan**: **Free**
3. Click **Create Database**.
4. Once created, copy the **Internal Database URL** (e.g. `postgresql://portfolio_user:...@dpg-...:5432/portfolio_db`).

#### 2. Create the Web Service on Render
1. Click **New +** $\rightarrow$ **Web Service**.
2. Select **Build and deploy from a Git repository** $\rightarrow$ Connect your repository.
3. Configure settings:
   - **Name**: `nagasrinivas-portfolio` (or your choice)
   - **Region**: Same region as your database
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn portfolio.wsgi:application --workers 2`
   - **Plan**: **Free**

4. Scroll down to **Environment Variables** and add:

| Key | Value | Description |
| :--- | :--- | :--- |
| `PYTHON_VERSION` | `3.12.8` | Python version on Render |
| `DJANGO_SETTINGS_MODULE` | `portfolio.settings.production` | Use production settings |
| `DEBUG` | `False` | Turn off debug mode for security |
| `SECRET_KEY` | *(Click "Generate" on Render or paste random string)* | Django secret key |
| `DATABASE_URL` | *(Paste Internal Database URL from step 1)* | Database connection string |
| `OPENROUTER_API_KEY` | `sk-or-v1-...` | Your OpenRouter API Key |
| `ALLOWED_HOSTS` | `.onrender.com` | Allowed domains |
| `CSRF_TRUSTED_ORIGINS` | `https://*.onrender.com` | Allowed CSRF origins |

5. Click **Create Web Service**.

---

## 4. Step 3: Environment Variables Reference

When deploying, your `.env` on Render needs:

```env
# Core Django
SECRET_KEY=your-random-generated-secret-key
DEBUG=False
DJANGO_SETTINGS_MODULE=portfolio.settings.production

# Domains & Security
ALLOWED_HOSTS=.onrender.com
CSRF_TRUSTED_ORIGINS=https://*.onrender.com

# PostgreSQL Connection
DATABASE_URL=postgresql://portfolio_user:password@host:5432/portfolio_db

# AI Chatbot
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Social URLs (optional defaults are already in base.py)
GITHUB_URL=https://github.com/NagasrinivasGovvala
LINKEDIN_URL=https://linkedin.com/in/nagasrinivas-govvala
CONTACT_EMAIL=nagasrinivas@email.com
```

---

## 5. Step 4: Create Django Admin Superuser on Render

Once your service status changes to **Live**:

1. In your Render Dashboard, click your Web Service (`nagasrinivas-portfolio`).
2. Go to the **Shell** tab on the left sidebar.
3. Run the following command:
   ```bash
   python manage.py createsuperuser
   ```
4. Enter your desired admin username, email, and password.
5. You can now log into your live admin panel at:
   `https://your-portfolio.onrender.com/admin/`

---

## 6. Step 5: Verify Your Live Portfolio

Check the following to ensure everything is working:
- **Homepage & 3D Canvas**: Visit `https://your-portfolio.onrender.com/` — check Three.js hero, smooth scrolling, and animations.
- **Projects & Media**: Check if project thumbnails, hover GIFs, and screenshots display.
- **Resume Download**: Click "Download CV" or view PDF.
- **Background Music**: Play/pause the audio track in the music widget.
- **AI Chatbot**: Open the chatbot modal and send a test message (e.g. *"What are Srinivas's top skills?"*).
- **Contact Form**: Submit a message to test validation and storage.

---

## 7. Optional: Keep Render Free Tier Active (No Cold Starts)

Render's free tier web services spin down after 15 minutes of inactivity. When a visitor arrives, it takes ~30–50 seconds to wake up.

To keep it warm and fast 24/7 for free:
1. Go to **[Cron-job.org](https://cron-job.org/)** or **[UptimeRobot](https://uptimerobot.com/)** (both free).
2. Create a monitor that sends an HTTP `GET` request to `https://your-portfolio.onrender.com/` every **10 minutes**.
3. Your portfolio will stay warm and respond instantly to recruiters!

---

## 8. Troubleshooting & Common Questions

### Q: Why did static files or styles fail to load?
**A**: Ensure WhiteNoise is active (it is configured in `portfolio/settings/production.py`) and `build.sh` ran `python manage.py collectstatic --no-input`.

### Q: Why do I get a 403 Forbidden CSRF verification failed error?
**A**: Ensure `CSRF_TRUSTED_ORIGINS=https://*.onrender.com` or your exact custom domain `https://yourdomain.com` is set in Render's Environment Variables.

### Q: How do I update my portfolio in the future?
**A**: Simply push changes to GitHub:
```bash
git add .
git commit -m "Update project details"
git push origin main
```
Render will automatically detect the push and redeploy your live site in ~2 minutes!
