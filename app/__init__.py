from flask import Flask, jsonify
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from config import Config
from datetime import datetime
import logging
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask extensions (global instances)
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    logger.info("Starting minimal Flask application...")
    
    # Normalize DATABASE_URL if present (postgres:// -> postgresql://)
    db_url = app.config.get('DATABASE_URL')
    if db_url:
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
        logger.info("Database URL configured and normalized")

    # Initialize extensions
    logger.info("Initializing login manager...")
    login_manager.init_app(app)
    
    logger.info("Initializing CSRF protection...")
    csrf.init_app(app)
    
    logger.info("Initializing mail...")
    mail.init_app(app)
    
    logger.info("Initializing SQLAlchemy and Migrate...")
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Configure login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Health check route
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'Application is running'})
    
    # Remove basic home route - let main blueprint handle it
    # @app.route('/')
    # def home():
    #     return '''
    #     <h1>Mayur Prabhune - Website</h1>
    #     <p>Application is running successfully!</p>
    #     <p><a href="/health">Health Check</a></p>
    #     <p>Domain: mayurprabhune.in</p>
    #     '''
    
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

    @app.context_processor
    def inject_site_settings():
        from app.site_settings import get_site_settings
        return {'site_settings': get_site_settings()}
    
    # Register blueprints - import them inside app context
    with app.app_context():
        try:
            from app.routes.main import bp as main_bp
            app.register_blueprint(main_bp)
            logger.info("Registered main blueprint")
        except Exception as e:
            logger.warning(f"Could not register main blueprint: {e}")
        
        try:
            from app.routes.auth import bp as auth_bp
            app.register_blueprint(auth_bp, url_prefix='/auth')
            logger.info("Registered auth blueprint")
        except Exception as e:
            logger.warning(f"Could not register auth blueprint: {e}")
        
        try:
            from app.routes.blog import bp as blog_bp
            app.register_blueprint(blog_bp, url_prefix='/blog')
            logger.info("Registered blog blueprint")
        except Exception as e:
            logger.warning(f"Could not register blog blueprint: {e}")
        
        try:
            from app.routes.admin import bp as admin_bp
            app.register_blueprint(admin_bp, url_prefix='/admin')
            logger.info("Registered admin blueprint")
        except Exception as e:
            logger.warning(f"Could not register admin blueprint: {e}")
    
    logger.info("Application initialized successfully")
    return app
