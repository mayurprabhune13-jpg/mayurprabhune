from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import Config
from datetime import datetime

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
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