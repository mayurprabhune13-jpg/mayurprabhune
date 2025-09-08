# Free Deployment Plan for mayurprabhune.in

## Overview
This plan focuses on free deployment platforms that support Git-based deployment for your Flask portfolio website. All options include custom domain support and SSL certificates.

## Recommended Free Platforms

### 1. Railway (railway.app) - **Top Choice**
- **Free Tier**: Yes, with 500 hours/month
- **Git Deployment**: Yes, via GitHub integration
- **Python Support**: Excellent
- **Custom Domain**: Free
- **SSL**: Automatic

### 2. Render (render.com) - **Good Alternative**
- **Free Tier**: Yes, with 750 hours/month
- **Git Deployment**: Yes, via GitHub/GitLab
- **Python Support**: Good
- **Custom Domain**: Free
- **SSL**: Automatic

### 3. Heroku (heroku.com) - **Requires Credit Card**
- **Free Tier**: Yes, but requires credit card verification
- **Git Deployment**: Yes, via Heroku CLI
- **Python Support**: Excellent
- **Custom Domain**: Free
- **SSL**: Automatic

## Step-by-Step Deployment Guide

### For Railway (Recommended)

#### Prerequisites
- GitHub account with repository pushed
- Railway account (free)

#### Deployment Steps
1. **Sign up at railway.app** using GitHub login
2. **Create new project** and connect your GitHub repository
3. **Configure environment variables** in Railway dashboard:
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secure-random-key
   ADMIN_EMAIL=mayur.prabhune@gmail.com
   ADMIN_PASSWORD=your-secure-password
   CONTACT_EMAIL=mayur.prabhune@gmail.com
   CONTACT_PHONE=+917620065818
   CONTACT_LINKEDIN=https://www.linkedin.com/in/mayur-prabhune
   ```
4. **Deploy automatically** - Railway will build and deploy on git push
5. **Add custom domain** in Railway project settings
6. **Configure DNS** at your registrar:
   - CNAME record: `www` → railway-provided URL

### For Render (Alternative)

#### Prerequisites
- GitHub account with repository
- Render account (free)

#### Deployment Steps
1. **Sign up at render.com** using GitHub login
2. **Create Web Service** and connect repository
3. **Build settings**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
4. **Set environment variables** in Render dashboard
5. **Deploy** - Automatic on git push
6. **Add custom domain** in Render settings
7. **Update DNS** with provided records

## DNS Configuration for Custom Domain

For both platforms, update your domain registrar's DNS settings:

1. **For Railway**:
   - Type: CNAME
   - Name: www
   - Value: [railway-provided URL]
   - TTL: 3600

2. **For Render**:
   - Follow the specific DNS records provided in Render dashboard

## Post-Deployment Checklist

- [ ] Verify website loads at `https://www.mayurprabhune.in`
- [ ] Check SSL certificate is valid and active
- [ ] Test all pages: Home, About, Services, Contact, Blog
- [ ] Test contact form functionality
- [ ] Verify admin login at `/admin/login`
- [ ] Test API endpoints
- [ ] Check mobile responsiveness
- [ ] Monitor application logs for errors

## Maintenance
- Regular git pushes for updates
- Monitor free tier usage limits
- Keep dependencies updated in requirements.txt
- Renew domain registration annually

## Immediate Next Steps
1. Choose Railway or Render based on preference
2. Create account on chosen platform
3. Connect GitHub repository
4. Set environment variables
5. Deploy and configure domain

This plan provides a straightforward path to free deployment with professional features.