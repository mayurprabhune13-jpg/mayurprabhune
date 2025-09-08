# Domain Deployment Plan for mayurprabhune.in

This guide provides step-by-step instructions for deploying your Flask portfolio website to the domain `https://www.mayurprabhune.in`.

## Prerequisites

- Registered domain: `mayurprabhune.in` (purchased from domain registrar)
- DNS management access
- Chosen deployment platform account (Heroku, Render, Railway, VPS, etc.)

## Deployment Options

### Option 1: Heroku Deployment with Custom Domain

#### Step 1: Deploy to Heroku
1. Create Heroku app:
   ```bash
   heroku create mayur-prabhune-portfolio
   ```

2. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-production-secret-key
   heroku config:set DATABASE_URL=your-postgresql-url
   heroku config:set ADMIN_EMAIL=mayur.prabhune@gmail.com
   heroku config:set ADMIN_PASSWORD=secure-production-password
   heroku config:set CONTACT_EMAIL=mayur.prabhune@gmail.com
   heroku config:set CONTACT_PHONE=+917620065818
   heroku config:set CONTACT_LINKEDIN=https://www.linkedin.com/in/mayur-prabhune
   ```

3. Deploy code:
   ```bash
   git push heroku main
   heroku run flask db upgrade
   ```

#### Step 2: Configure Custom Domain
1. In Heroku dashboard, go to Settings → Domains
2. Add domain: `www.mayurprabhune.in`
3. Heroku will provide DNS target (e.g., `example.herokudns.com`)

#### Step 3: DNS Configuration
1. Log into your domain registrar's DNS management
2. Create CNAME record:
   - Type: CNAME
   - Name: www
   - Value: Heroku DNS target (e.g., `example.herokudns.com`)
   - TTL: 3600

3. Create redirect for root domain (optional):
   - Type: URL Redirect
   - From: `mayurprabhune.in` 
   - To: `https://www.mayurprabhune.in`

#### Step 4: SSL Certificate
- Heroku automatically provides SSL certificates for custom domains
- Verify SSL is active in Heroku dashboard

### Option 2: Render Deployment with Custom Domain

#### Step 1: Deploy to Render
1. Connect repository to Render
2. Create Web Service with settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn wsgi:app`
   - Environment Variables: Set same as Heroku above

#### Step 2: Domain Configuration
1. In Render dashboard, go to Settings → Domains
2. Add custom domain: `www.mayurprabhune.in`
3. Render will provide DNS records

#### Step 3: DNS Setup
Update DNS records at your registrar:
- CNAME record for `www` pointing to Render's provided URL
- A/AAAA records for root domain if supported

### Option 3: Traditional VPS Deployment (DigitalOcean/AWS)

#### Step 1: Server Setup
1. Create Ubuntu 22.04 server
2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx certbot python3-certbot-nginx
   ```

#### Step 2: Application Deployment
1. Clone repository:
   ```bash
   git clone https://github.com/your-repo/mayur-prabhune.git
   cd mayur-prabhune
   ```

2. Set up virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements-prod.txt
   ```

3. Configure environment variables in `.env`:
   ```env
   FLASK_ENV=production
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://user:pass@localhost:5432/mayurdb
   ADMIN_EMAIL=mayur.prabhune@gmail.com
   ADMIN_PASSWORD=secure-password
   ```

#### Step 3: Nginx Configuration
Create `/etc/nginx/sites-available/mayurprabhune.in`:
```nginx
server {
    listen 80;
    server_name mayurprabhune.in www.mayurprabhune.in;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /path/to/your/app/static;
    }
}
```

#### Step 4: SSL with Let's Encrypt
```bash
sudo certbot --nginx -d mayurprabhune.in -d www.mayurprabhune.in
```

#### Step 5: Gunicorn Service
Create `/etc/systemd/system/mayurprabhune.service`:
```ini
[Unit]
Description=Gunicorn instance for Mayur Prabhune
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/path/to/mayur-prabhune
Environment="PATH=/path/to/mayur-prabhune/venv/bin"
ExecStart=/path/to/mayur-prabhune/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:app

[Install]
WantedBy=multi-user.target
```

### Option 4: Railway Deployment

#### Step 1: Deploy to Railway
1. Connect repository
2. Set environment variables in Railway dashboard
3. Deploy automatically

#### Step 2: Domain Configuration
1. In Railway project settings, add custom domain
2. Update DNS records as instructed by Railway

## DNS Configuration Details

For all platforms, ensure DNS records are properly set:

1. **For Heroku/Render/Railway**:
   - CNAME for `www` → platform-specific DNS target
   - Redirect root domain to `www`

2. **For VPS**:
   - A record for `@` → server IP address
   - A record for `www` → server IP address
   - Or CNAME for `www` → domain name

## Environment Variables for Production

Update your `.env` or platform environment variables:

```env
FLASK_ENV=production
SECRET_KEY=generate-secure-random-key
DATABASE_URL=postgresql://user:password@host:port/database
ADMIN_EMAIL=mayur.prabhune@gmail.com
ADMIN_PASSWORD=change-this-in-production
CONTACT_EMAIL=mayur.prabhune@gmail.com
CONTACT_PHONE=+917620065818
CONTACT_LINKEDIN=https://www.linkedin.com/in/mayur-prabhune
```

## Post-Deployment Checklist

- [ ] Verify website loads at `https://www.mayurprabhune.in`
- [ ] Check SSL certificate is valid
- [ ] Test all pages (Home, About, Services, Contact, Blog)
- [ ] Test contact form functionality
- [ ] Verify admin login at `/admin/login`
- [ ] Check API endpoints are working
- [ ] Test mobile responsiveness
- [ ] Verify Google Analytics (if added)
- [ ] Set up monitoring and error tracking

## Maintenance

- Regular backups of database
- Monitor application logs
- Keep dependencies updated
- Renew SSL certificates automatically
- Scale resources as traffic grows

## Support Resources

- Domain registrar: DNS management help
- Deployment platform: Their documentation
- Flask documentation: For application issues
- Let's Encrypt: For SSL certificate issues

This plan provides a comprehensive guide for deploying your portfolio website to your custom domain with professional-grade setup.