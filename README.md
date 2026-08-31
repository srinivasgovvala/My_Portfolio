# Portfolio for Nagasrinivas Govvala

A full-stack personal portfolio built with Django, Three.js, and GSAP.

## Stack

- **Backend:** Python 3.14, Django 5.2, SQLite (dev) / PostgreSQL (prod)
- **Frontend:** Django Templates, HTML5, CSS3, JavaScript, Three.js, GSAP
- **AI Chatbot:** OpenRouter API
- **Media:** Django media storage

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed initial data
python seed_data.py

# Update media paths (after copying assets)
python update_media.py

# Create admin user
python manage.py createsuperuser

# Start dev server
python manage.py runserver
```

## Admin

Visit `/admin/` to manage all portfolio content: projects, skills, education, music tracks, chatbot settings, and more.

## Environment Variables

Create a `.env` file or set these in your environment:

```
SECRET_KEY=your-secret-key
OPENROUTER_API_KEY=your-openrouter-key (for AI chatbot)
GITHUB_URL=https://github.com/YourProfile
LINKEDIN_URL=https://linkedin.com/in/YourProfile
CONTACT_EMAIL=your@email.com
```

## Production

Use `portfolio.settings.production` and set `DATABASE_URL` for PostgreSQL.
