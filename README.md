# Mayur Prabhune - Portfolio Website

## 🚀 Current Status: Ready for Deployment

**⚠️ Deployment Status**: Application fully developed, awaiting Railway plan upgrade
- ✅ Complete Flask portfolio website with admin panel
- ✅ Domain configured: mayurprabhune.in
- ✅ Email service active: info@mayurprabhune.in (Titan Email)
- ✅ Database configured: PostgreSQL on Railway
- ❌ Deployment blocked: Railway account plan limitations

**Quick Solutions**: [See Deployment Options →](FINAL_DEPLOYMENT_RECOMMENDATIONS.md)

---

## Features

- **Responsive Design**: Modern, mobile-friendly interface built with TailwindCSS
- **Admin Dashboard**: Full CRUD operations for managing content
- **Content Management**: Blog posts, videos, testimonials, case studies, and contact messages
- **RESTful API**: JSON API endpoints for frontend integration
- **User Authentication**: Secure admin login with Flask-Login
- **Email Integration**: Contact form with Titan Email service
- **File Uploads**: Support for image and video uploads
- **Database Migrations**: Flask-Migrate for schema changes
- **SEO Optimized**: Slug-based URLs and meta tags
- **Custom Domain**: mayurprabhune.in with SSL ready

## Quick Deployment Options

### Option 1: Railway (Recommended - 5 minutes)
```bash
# Upgrade Railway plan ($5/month) then:
railway up
# Result: Live at mayurprabhune.in with SSL
```

### Option 2: Local Development
```bash
git clone <repository-url>
cd mayur-prabhune
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
# Access at: http://localhost:5000
```

### Option 3: Alternative Platforms
- **Render**: Free tier available (see [deployment guide](FINAL_DEPLOYMENT_RECOMMENDATIONS.md))
- **DigitalOcean**: $5/month with custom domain
- **Vercel/Netlify**: For static deployment options

## Tech Stack

- **Backend**: Python 3.8+, Flask, SQLAlchemy, Gunicorn
- **Frontend**: HTML5, TailwindCSS, JavaScript (responsive design)
- **Database**: PostgreSQL (Railway), SQLite (development)
- **Email**: Flask-Mail with Titan Email SMTP
- **Authentication**: Flask-Login, secure session management
- **File Handling**: Werkzeug, Pillow for uploads
- **API**: RESTful JSON endpoints
- **Deployment**: Railway (configured), WSGI compatible

## Project Status & Documentation

### Key Documents
- 📋 **[Deployment Status](DEPLOYMENT_STATUS.md)** - Current technical status & issues
- 🎯 **[Final Recommendations](FINAL_DEPLOYMENT_RECOMMENDATIONS.md)** - Deployment solutions & pricing
- 🏗️ **[Architecture Guide](project_architecture.md)** - Technical documentation
- 🌐 **[Domain Setup](DOMAIN_DEPLOYMENT.md)** - DNS & custom domain configuration

### Current Configuration (Production Ready)
```env
✅ DATABASE_URL=postgresql://[configured on Railway]
✅ MAIL_SERVER=smtp.titan.email
✅ MAIL_USERNAME=info@mayurprabhune.in  
✅ MAIL_PASSWORD=[configured]
✅ ADMIN_USERNAME=admin
✅ ADMIN_PASSWORD=[configured]
✅ SECRET_KEY=[configured]
✅ Domain: mayurprabhune.in (DNS configured)
```

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
   ADMIN_EMAIL=mayur.prabhune@gmail.com
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
   # or: python run.py
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

## Production Deployment

### Current Status: Railway (Configured, Needs Plan Upgrade)
All configuration is complete on Railway:
- Environment variables set
- Database connected
- Domain configured
- **Issue**: Plan limitation preventing deployment

**Solution**: Upgrade to Railway Developer plan ($5/month) → Instant deployment

### Alternative Platforms

#### Render
1. Create account at render.com
2. Connect GitHub repository
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn wsgi:app`
5. Add environment variables
6. Custom domain: Requires paid plan ($7/month)

#### DigitalOcean App Platform
1. Create DigitalOcean account
2. Deploy from GitHub
3. Configure build settings
4. Add environment variables
5. Custom domain included ($5/month)

#### Traditional VPS
1. Install Gunicorn: `pip install gunicorn`
2. Run: `gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app`
3. Set up reverse proxy with Nginx/Apache

## File Structure

```
mayur-prabhune/
├── app/                    # Application package
│   ├── __init__.py        # Flask app factory
│   ├── models.py          # Database models
│   ├── utils.py          # Utility functions
│   ├── monitoring.py     # Health checks & monitoring
│   ├── routes/            # Blueprint routes
│   │   ├── main.py       # Main routes
│   │   ├── admin.py      # Admin routes
│   │   ├── api.py        # API routes
│   │   ├── auth.py       # Authentication routes
│   │   └── blog.py       # Blog routes
│   ├── static/           # Static files
│   │   ├── uploads/     # Uploaded files
│   │   └── images/      # Static images
│   └── templates/        # Jinja2 templates
│       ├── base.html     # Base template
│       ├── index.html    # Home page
│       ├── admin/        # Admin templates
│       ├── auth/         # Auth templates
│       ├── errors/       # Error pages
│       └── ...          # Other templates
├── migrations/           # Database migrations
├── simple_app.py        # Minimal test application
├── config.py            # Development configuration
├── config_prod.py       # Production configuration
├── run.py               # Development entry point
├── wsgi.py              # Production WSGI entry point
├── Procfile             # Railway/Heroku deployment config
├── requirements.txt     # Development dependencies
├── requirements-prod.txt # Production dependencies
├── DEPLOYMENT_STATUS.md  # Current deployment status
├── FINAL_DEPLOYMENT_RECOMMENDATIONS.md # Solutions guide
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Next Steps

1. **Immediate**: Choose deployment platform
   - Railway upgrade ($5/month) - recommended for speed
   - Render free tier - budget option
   - DigitalOcean ($5/month) - full control

2. **Deploy**: Follow platform-specific instructions in [Final Recommendations](FINAL_DEPLOYMENT_RECOMMENDATIONS.md)

3. **Test**: Use post-deployment checklist to verify functionality

4. **Monitor**: Application includes health checks and error handling

## Important Environment Variables

Set in `.env` (examples):

```env
FLASK_ENV=development
SECRET_KEY=change-me-in-production
DATABASE_URL=sqlite:///app.db
ADMIN_USERNAME=admin
ADMIN_EMAIL=mayur.prabhune@gmail.com
ADMIN_PASSWORD=secure-password

# Email Configuration (Titan Email - configured)
MAIL_SERVER=smtp.titan.email
MAIL_PORT=587
MAIL_USERNAME=info@mayurprabhune.in
MAIL_PASSWORD=your-email-password
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER=info@mayurprabhune.in

# Optional contact info exposed to templates
CONTACT_EMAIL=mayur.prabhune@gmail.com
CONTACT_PHONE=+91 7620065818
CONTACT_LINKEDIN=https://www.linkedin.com/in/mayur-prabhune
```

## Support & Cost Analysis

### Monthly Hosting Costs
| Platform | Cost | Custom Domain | SSL | Database | Email |
|----------|------|---------------|-----|----------|-------|
| Railway Developer | $5 | ✅ Free | ✅ Auto | ✅ Included | ✅ Configured |
| Render Starter | $7 | ✅ Included | ✅ Auto | $7 extra | External |
| DigitalOcean | $5 | ✅ Included | ✅ Auto | $15 extra | External |

**Recommendation**: Railway upgrade for immediate deployment with all features.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For support and questions:
- **Email**: info@mayurprabhune.in (active)
- **Website**: mayurprabhune.in (pending deployment)
- **LinkedIn**: https://www.linkedin.com/in/mayur-prabhune

---

**Last Updated**: January 13, 2025  
**Status**: Production-ready, awaiting deployment platform decision  
**Quick Start**: See [FINAL_DEPLOYMENT_RECOMMENDATIONS.md](FINAL_DEPLOYMENT_RECOMMENDATIONS.md)