from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config
from datetime import datetime
from app.monitoring import Monitoring

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
monitoring = Monitoring()
mail = Mail()

def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Handle DATABASE_URL format for PostgreSQL
    try:
        if app.config.get('DATABASE_URL'):
            logger.info("Configuring database connection...")
            db_url = app.config['DATABASE_URL']
            
            if db_url.startswith('postgres://'):
                db_url = db_url.replace('postgres://', 'postgresql://', 1)
                logger.info("Converted postgres:// to postgresql://")
            
            # Add connection pooling parameters
            if '?' not in db_url:
                db_url += '?pool_size=10&pool_timeout=30&pool_pre_ping=true'
            logger.info("Added connection pooling parameters")
            
            app.config['SQLALCHEMY_DATABASE_URI'] = db_url
            app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
                'pool_size': 10,
                'pool_timeout': 30,
                'pool_pre_ping': True
            }
            logger.info(f"Database URL configured: {db_url.split('@')[0]}@[HIDDEN]")
        else:
            logger.warning("No DATABASE_URL configured, using SQLite")
    
    # Initialize extensions with app
    try:
        logger.info("Initializing database...")
        db.init_app(app)
        
        logger.info("Initializing migrations...")
        migrate.init_app(app, db)
        
        logger.info("Initializing login manager...")
        login_manager.init_app(app)
        
        logger.info("Initializing CSRF protection...")
        csrf.init_app(app)
        
        logger.info("Initializing monitoring...")
        monitoring.init_app(app)
        
        logger.info("Initializing mail...")
        mail.init_app(app)
        
        # Test database connection with retry
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                with app.app_context():
                    db.engine.connect()
                    logger.info("Database connection test successful")
                    break
            except Exception as conn_err:
                retry_count += 1
                if retry_count == max_retries:
                    logger.error(f"Failed to connect to database after {max_retries} attempts")
                    raise
                logger.warning(f"Database connection attempt {retry_count} failed: {str(conn_err)}")
                from time import sleep
                sleep(2 ** retry_count)  # Exponential backoff
            
    except Exception as e:
        logger.error(f"Error during initialization: {str(e)}")
        raise
    
    # Configure login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Global template variables
    @app.context_processor
    def inject_contact_info():
        return {
            'CONTACT_EMAIL': app.config.get('ADMIN_EMAIL', 'admin@example.com'),
            'CONTACT_PHONE': app.config.get('CONTACT_PHONE', ''),
            'CONTACT_LINKEDIN': app.config.get('CONTACT_LINKEDIN', '')
        }
    
    # Add context processor to make 'now' available in all templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    
    # Register blueprints
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.routes.blog import bp as blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')
    
    from app.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.routes.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Initialize database
    with app.app_context():
        # Create admin user if it doesn't exist
        from app.models import User
        admin = User.query.filter_by(username=app.config['ADMIN_USERNAME']).first()
        if not admin:
            admin = User(
                username=app.config['ADMIN_USERNAME'],
                email=app.config['ADMIN_EMAIL'],
                is_admin=True
            )
            db.session.add(admin)
        admin.set_password(app.config['ADMIN_PASSWORD'])
        db.session.commit()
    
    return app

from app import models  # Import models after db is defined