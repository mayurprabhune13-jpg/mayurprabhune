"""
WSGI entry point for production deployment
"""
import os
from app import create_app
from config_prod import ProductionConfig

# Create application instance with production configuration
app = create_app(ProductionConfig)

if __name__ == '__main__':
    # This allows running with python wsgi.py for testing
    app.run()