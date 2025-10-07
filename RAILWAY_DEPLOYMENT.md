# Railway Deployment Guide - Mayur Prabhune AI Mentor Website

## Prerequisites
- Railway account (sign up at https://railway.app)
- Git repository with the project
- GitHub account for repository hosting

## Step 1: Prepare Your Project

### Files Created for Deployment
✅ `requirements.txt` - Python dependencies
✅ `Procfile` - Process configuration for Railway
✅ `runtime.txt` - Python version specification
✅ `railway.json` - Railway-specific configuration
✅ `.gitignore` - Git ignore rules

### Environment Variables Needed
Create these environment variables in Railway:
- `FLASK_ENV=production`
- `SECRET_KEY=your-secure-secret-key-here`
- `DATABASE_URL=postgresql://...` (Railway will provide this)

## Step 2: Deploy to Railway

### Option A: Deploy from GitHub (Recommended)

1. **Repository Ready**:
   ✅ Code already pushed to: https://github.com/mayurprabhune13-jpg/mayurprabhune.git
   ✅ Python 3.11 compatibility fixes applied
   ✅ Docker configuration included

2. **Deploy on Railway**:
   - Visit https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose repository: `mayurprabhune13-jpg/mayurprabhune`
   - Railway will use the Dockerfile for Python 3.11 deployment

### Option B: Deploy with Railway CLI

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Deploy**:
   ```bash
   railway login
   railway init
   railway up
   ```

## Step 3: Configure Environment Variables

In Railway dashboard:
1. Go to your project
2. Click "Variables" tab
3. Add these variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=generate-a-secure-random-key
   ```

## Step 4: Database Setup

Railway will automatically provide a PostgreSQL database:
1. In Railway dashboard, click "Add Database" → "PostgreSQL"
2. Railway will set the `DATABASE_URL` environment variable automatically
3. Your app will use this for production

## Step 5: Initialize Database

After deployment, visit your app URL + `/setup-db` to initialize the database:
```
https://your-app-name.railway.app/setup-db
```

## Step 6: Custom Domain (Optional)

1. In Railway dashboard, go to "Settings"
2. Click "Domains"
3. Add your custom domain (e.g., mayurprabhune.in)
4. Update DNS records as instructed

## Expected Deployment Configuration

### Production URLs
- **Main Site**: `https://your-app-name.railway.app`
- **Admin Panel**: `https://your-app-name.railway.app/admin`
- **Database Setup**: `https://your-app-name.railway.app/setup-db`

### Automatic Features
- ✅ HTTPS/SSL certificates automatically provided
- ✅ CDN and global distribution
- ✅ Automatic scaling based on traffic
- ✅ Health checks and monitoring
- ✅ Automatic restarts on failure

## Environment Configuration

### Production Settings (`config_prod.py`)
The app will automatically use production settings when `FLASK_ENV=production`:
- PostgreSQL database instead of SQLite
- Enhanced security settings
- Optimized for performance
- Proper error handling

### Static Files
Railway will serve static files automatically from `/static/` directory.

## Monitoring and Maintenance

### Logs
View logs in Railway dashboard:
1. Go to your project
2. Click "Deployments"
3. Click on latest deployment
4. View real-time logs

### Database Management
Access database via Railway dashboard:
1. Go to your project
2. Click on PostgreSQL service
3. Use "Connect" to get connection details
4. Can use tools like pgAdmin or command line

## GEO Optimization in Production

### Schema Markup Validation
After deployment, validate schema markup:
1. Visit https://search.google.com/test/rich-results
2. Enter your production URL
3. Verify all schema types are detected:
   - Person Schema (Mayur Prabhune)
   - LocalBusiness Schema
   - Service Schema
   - FAQ Schema
   - Organization Schema

### Performance Optimization
Railway automatically provides:
- ✅ HTTP/2 support
- ✅ Gzip compression
- ✅ Global CDN
- ✅ Fast static file serving

## Troubleshooting

### Common Issues

1. **Build Fails**:
   - Check `requirements.txt` for correct versions
   - Ensure `runtime.txt` specifies supported Python version

2. **App Won't Start**:
   - Verify `Procfile` points to correct WSGI file
   - Check environment variables are set

3. **Database Errors**:
   - Ensure PostgreSQL service is added
   - Run `/setup-db` endpoint after deployment
   - Check `DATABASE_URL` environment variable

4. **Static Files Not Loading**:
   - Verify files are in `app/static/` directory
   - Check `.gitignore` isn't excluding static files

### Support
- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Railway GitHub: https://github.com/railwayapp/railway

## Post-Deployment Checklist

### Immediate Actions
- [ ] Visit homepage and verify it loads correctly
- [ ] Test all navigation links
- [ ] Verify contact form works
- [ ] Check admin panel access
- [ ] Validate schema markup with Google tools

### SEO and Marketing
- [ ] Submit sitemap to Google Search Console
- [ ] Update Google Business Profile with new URL
- [ ] Update LinkedIn profile with website URL
- [ ] Set up Google Analytics (if desired)
- [ ] Configure domain redirects (if using custom domain)

### Ongoing Maintenance
- [ ] Monitor Railway usage and costs
- [ ] Set up automated backups for database
- [ ] Regular security updates for dependencies
- [ ] Monitor website performance and uptime

---

## Quick Deploy Commands

```bash
# 1. Initialize git and push to GitHub
git init
git add .
git commit -m "Deploy Mayur Prabhune AI Mentor site with GEO optimization"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main

# 2. Deploy to Railway (using CLI)
npm install -g @railway/cli
railway login
railway init
railway up

# 3. Add environment variables via Railway dashboard
# FLASK_ENV=production
# SECRET_KEY=your-secret-key

# 4. Initialize database
# Visit: https://your-app.railway.app/setup-db
```

**Deployment Status**: Ready for Railway deployment
**Expected Deploy Time**: 3-5 minutes
**GEO Features**: All 7 phases included and validated