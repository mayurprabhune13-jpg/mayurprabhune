# Website Architecture Plan

## Project Structure
```
mayur-prabhune-website/
├── app/
│   ├── __init__.py           # Flask application initialization
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py          # Main routes (home, about, services)
│   │   ├── blog.py          # Blog related routes
│   │   ├── admin.py         # Admin panel routes
│   │   └── api.py           # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User model for admin
│   │   ├── blog.py          # Blog post model
│   │   └── testimonial.py   # Testimonial model
│   ├── templates/
│   │   ├── base.html        # Base template with common elements
│   │   ├── index.html       # Home page
│   │   ├── about.html       # About page
│   │   ├── services.html    # Services page
│   │   ├── blog/
│   │   │   ├── list.html    # Blog listing
│   │   │   └── post.html    # Individual post
│   │   └── admin/
│   │       ├── login.html
│   │       ├── dashboard.html
│   │       └── videos.html
│   └── static/
│       ├── css/
│       │   └── styles.css   # Compiled styles
│       ├── js/
│       │   └── main.js      # Frontend JavaScript
│       └── images/
├── config.py                 # Configuration settings
├── requirements.txt         # Python dependencies
└── run.py                  # Application entry point

## Components

### Frontend
1. Templates (Jinja2)
   - Base template with shared components
   - Page-specific templates
   - Reusable components

2. Static Assets
   - TailwindCSS (via CDN)
   - Custom CSS for specific components
   - JavaScript for interactivity
   - Images and media files

3. Components
   - Navigation header
   - Footer
   - Video thumbnails
   - Contact forms
   - Blog post cards
   - Admin dashboard widgets

### Backend (Flask)

1. Core Features
   - Route handling
   - Template rendering
   - Form processing
   - Admin authentication
   - File uploads (for blog/videos)

2. Data Models
   - Users (admin)
   - Blog posts
   - Testimonials
   - Success stories
   - Videos

3. API Endpoints
   - Blog management
   - Testimonial submission
   - Contact form handling
   - Video management

### Security Features
1. Admin Authentication
   - Secure login system
   - Session management
   - Protected routes

2. Form Security
   - CSRF protection
   - Input validation
   - Rate limiting

3. Data Protection
   - Secure password storage
   - Environment variables
   - Config management

## Database Schema

1. Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL
);
```

2. Blog Posts Table
```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    author_id INTEGER REFERENCES users(id)
);
```

3. Testimonials Table
```sql
CREATE TABLE testimonials (
    id INTEGER PRIMARY KEY,
    author VARCHAR(100) NOT NULL,
    role VARCHAR(100),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

4. Videos Table
```sql
CREATE TABLE videos (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    thumbnail_url VARCHAR(500),
    video_url VARCHAR(500) NOT NULL,
    category VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Implementation Steps

1. Setup Development Environment
   - Python virtual environment
   - Install Flask and dependencies
   - Configure development server

2. Create Base Structure
   - Initialize Flask application
   - Set up configuration
   - Create database models
   - Implement base template

3. Implement Frontend
   - Convert existing HTML to templates
   - Implement responsive design
   - Add interactive features
   - Style components

4. Develop Backend Features
   - Set up routes
   - Implement authentication
   - Create API endpoints
   - Add form handling

5. Testing & Optimization
   - Test all features
   - Optimize performance
   - Security checks
   - Cross-browser testing

6. Deployment
   - Server setup
   - Database configuration
   - Static file serving
   - SSL certificate