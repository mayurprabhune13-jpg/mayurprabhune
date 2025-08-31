# Mayur Prabhune - Portfolio Website

A comprehensive Flask-based portfolio website with admin dashboard, content management system, and RESTful API.

## Features

- **Responsive Design**: Modern, mobile-friendly interface built with TailwindCSS
- **Admin Dashboard**: Full CRUD operations for managing content
- **Content Management**: Blog posts, videos, testimonials, case studies, and contact messages
- **RESTful API**: JSON API endpoints for frontend integration
- **User Authentication**: Secure admin login with Flask-Login
- **File Uploads**: Support for image and video uploads
- **Database Migrations**: Flask-Migrate for schema changes
- **SEO Optimized**: Slug-based URLs and meta tags

## Tech Stack

- **Backend**: Python 3.8+, Flask, SQLAlchemy
- **Frontend**: HTML5, TailwindCSS, JavaScript
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Authentication**: Flask-Login, Flask-WTF
- **File Uploads**: Werkzeug, Pillow
- **API**: RESTful JSON API
- **Deployment**: Gunicorn, WSGI compatible

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mayur-prabhune
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Environment configuration**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` file with your configuration:
   ```env
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///app.db
   ADMIN_USERNAME=admin
   ADMIN_EMAIL=admin@example.com
   ADMIN_PASSWORD=admin
   ```

6. **Initialize database**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

7. **Run development server**
   ```bash
   flask run
   ```
   The application will be available at `http://127.0.0.1:5000`

## Admin Access

Access the admin dashboard at `/admin/login` with the following credentials:
- **Username**: admin
- **Password**: admin

**Important**: Change the default admin password in production!

### Admin Features
- Manage blog posts with rich text editor
- Upload and manage videos
- Add/edit testimonials
- Create case studies with images
- View and respond to contact messages
- Content status management (published/draft/pending)

## API Endpoints

The application provides RESTful API endpoints at `/api/`:

### Blog Posts
- `GET /api/posts` - List all published posts
- `GET /api/posts/<slug>` - Get specific post
- `GET /api/posts?status=draft` - Filter by status

### Videos
- `GET /api/videos` - List all videos
- `GET /api/videos/<id>` - Get specific video

### Testimonials
- `GET /api/testimonials` - List all testimonials
- `POST /api/testimonials` - Create new testimonial (authenticated)

### Case Studies
- `GET /api/case-studies` - List all case studies
- `GET /api/case-studies/<slug>` - Get specific case study

## Deployment

### Production Deployment

1. **Install production dependencies**
   ```bash
   pip install -r requirements-prod.txt
   ```

2. **Set environment variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-production-secret-key
   export DATABASE_URL=your-production-database-url
   ```

3. **Database migration** (if using SQLite in production)
   ```bash
   flask db upgrade
   ```

### Deployment Platforms

#### Heroku
1. Create `Procfile` with:
   ```
   web: gunicorn wsgi:app
   ```
2. Set environment variables in Heroku dashboard
3. Deploy using Git push

#### PythonAnywhere
1. Upload project files
2. Configure virtual environment
3. Set up WSGI configuration file
4. Reload application

#### Traditional VPS
1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```
2. Run with:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
   ```
3. Set up reverse proxy with Nginx/Apache

## File Structure

```
mayur-prabhune/
├── app/                    # Application package
│   ├── __init__.py        # Flask app factory
│   ├── models.py          # Database models
│   ├── utils.py          # Utility functions
│   ├── routes/            # Blueprint routes
│   │   ├── main.py       # Main routes
│   │   ├── admin.py      # Admin routes
│   │   ├── api.py        # API routes
│   │   ├── auth.py       # Authentication routes
│   │   └── blog.py       # Blog routes
│   ├── static/           # Static files
│   │   ├── uploads/     # Uploaded files
│   │   └── ...          # Other static assets
│   └── templates/        # Jinja2 templates
│       ├── base.html     # Base template
│       ├── index.html    # Home page
│       ├── admin/        # Admin templates
│       ├── auth/         # Auth templates
│       └── ...          # Other templates
├── migrations/           # Database migrations
├── instance/            # Instance folder (database)
├── config.py            # Development configuration
├── config_prod.py       # Production configuration
├── run.py               # Development entry point
├── wsgi.py              # Production WSGI entry point
├── requirements.txt      # Development dependencies
├── requirements-prod.txt # Production dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact:
- Email: admin@example.com
- Website: https://your-domain.com

## Changelog

### v1.0.0
- Initial release with complete portfolio website
- Admin dashboard with full CRUD operations
- RESTful API endpoints
- Database migration system
- Production deployment configuration

---

## Quick Start (Windows)

1. Create and activate venv
   ```powershell
   py -m venv .venv
   . .venv\\Scripts\\Activate.ps1
   ```
2. Install deps
   ```powershell
   pip install -r requirements.txt
   ```
3. Configure env
   ```powershell
   copy .env.example .env
   # then edit .env
   ```
4. Initialize DB and run
   ```powershell
   flask db upgrade
   flask run
   # or: python run.py
   ```

## Important Environment Variables

Set in `.env` (examples):

```
FLASK_ENV=development
SECRET_KEY=change-me
DATABASE_URL=sqlite:///app.db
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin

# Optional contact info exposed to templates via context processor
CONTACT_EMAIL=admin@example.com
CONTACT_PHONE=+1-555-0100
CONTACT_LINKEDIN=https://www.linkedin.com/in/your-handle/
```

## Deployment (Render/Railway)

The app uses `wsgi.py` and Gunicorn (`gunicorn wsgi:app`).

### Render
1. New Web Service → Connect repo
2. Environment: `Python 3.x`
3. Build Command:
   ```
   pip install -r requirements.txt
   ```
4. Start Command:
   ```
   gunicorn wsgi:app
   ```
5. Add environment variables from `.env` (use a managed Postgres URL for production)

### Railway
1. New Project → Deploy from repo
2. Add a Service → `Python`
3. Variables: copy from `.env` and set `PORT` if required by buildpack
4. Start Command:
   ```
   gunicorn wsgi:app --bind 0.0.0.0:$PORT
   ```

## Notes

- Error templates live at `app/templates/errors/404.html` and `app/templates/errors/500.html`.
- New public templates include `videos.html`, `video_detail.html`, `testimonials.html`, and `post_detail.html`.
- Service CTAs in `templates/services.html` currently link to `main.contact` until dedicated pages are added.