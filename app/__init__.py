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
    try:
        app = Flask(__name__)
        app.config.from_object(config_class)
        
        # Configure database connection
        if app.config.get('DATABASE_URL'):
            logger.info("Configuring database connection...")
            db_url = app.config['DATABASE_URL']
            
            # Simple URL transformation
            if db_url.startswith('postgres://'):
                db_url = db_url.replace('postgres://', 'postgresql://', 1)
                logger.info("Converted postgres:// to postgresql://")
            
            app.config['SQLALCHEMY_DATABASE_URI'] = db_url
            logger.info(f"Database URL configured: {db_url.split('@')[0]}@[HIDDEN]")
        else:
            logger.warning("No DATABASE_URL configured, using SQLite")
            
        # Initialize extensions
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

        # Initialize database and admin user
        with app.app_context():
            logger.info("Creating database tables...")
            db.create_all()
            
            logger.info("Creating admin user...")
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
            logger.info("Admin user configured successfully")
        
        logger.info("Application initialized successfully")
        return app
        
    except Exception as e:
        logger.error(f"Application initialization error: {str(e)}")
        raise

from app import models  # Import models after db is defined