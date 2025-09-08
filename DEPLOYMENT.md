# Deployment Guide

This guide covers deploying the Flask application to various platforms.

## Prerequisites

- Python 3.8+
- PostgreSQL (recommended for production) or SQLite
- Git

## Environment Setup

1. Copy `.env.example` to `.env` and update with your actual values:
   ```bash
   cp .env.example .env
   ```

2. Set environment variables in `.env`:
   - `SECRET_KEY`: Generate a strong random key
   - `DATABASE_URL`: Database connection string (e.g., `postgresql://user:pass@localhost/dbname`)
   - `ADMIN_USERNAME`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`: Admin credentials
   - Mail settings if using email features

## Local Production Setup

1. Install production dependencies:
   ```bash
   pip install -r requirements-prod.txt
   ```

2. Initialize database:
   ```bash
   flask db upgrade
   ```

3. Run with Gunicorn:
   ```bash
   gunicorn wsgi:app
   ```

## Deployment to Heroku

1. Install Heroku CLI and login.

2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

3. Set environment variables on Heroku:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DATABASE_URL=your-database-url
   heroku config:set ADMIN_USERNAME=admin
   heroku config:set ADMIN_EMAIL=mayur.prabhune@gmail.com
   heroku config:set ADMIN_PASSWORD=securepassword
   ```

4. Deploy:
   ```bash
   git push heroku main
   ```

5. Run migrations:
   ```bash
   heroku run flask db upgrade
   ```

## Deployment to PythonAnywhere

1. Upload your code to PythonAnywhere.

2. Set up a virtual environment and install dependencies:
   ```bash
   pip install -r requirements-prod.txt
   ```

3. Configure the web app via the dashboard:
   - Source code: your project directory
   - Virtualenv: path to your virtual environment
   - WSGI file: `wsgi.py`

4. Set environment variables in the WSGI file or via the dashboard.

## Deployment with Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements-prod.txt .
RUN pip install -r requirements-prod.txt

COPY . .

CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000"]
```

Build and run:
```bash
docker build -t your-app .
docker run -d -p 5000:5000 --env-file .env your-app
```

## Notes

- Always use a strong `SECRET_KEY` in production.
- For production, use a proper database like PostgreSQL instead of SQLite.
- Ensure `DEBUG=False` in production.
- Set up proper logging and monitoring.