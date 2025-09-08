#!/usr/bin/env python3
"""
Script to check admin user details in the database.
"""
import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

def check_admin_user():
    app = create_app()
    with app.app_context():
        admin_username = app.config.get('ADMIN_USERNAME', 'admin')
        admin_user = User.query.filter_by(username=admin_username).first()
        
        if admin_user:
            print(f"Admin user found:")
            print(f"Username: {admin_user.username}")
            print(f"Email: {admin_user.email}")
            print(f"Is Admin: {admin_user.is_admin}")
            print(f"Password hash: {admin_user.password_hash}")
            
            # Test password check
            test_password = app.config.get('ADMIN_PASSWORD', 'change-in-production')
            password_correct = admin_user.check_password(test_password)
            print(f"Password check with '{test_password}': {'CORRECT' if password_correct else 'INCORRECT'}")
        else:
            print("Admin user not found in database.")
            print("Creating admin user...")
            admin_email = app.config.get('ADMIN_EMAIL', 'admin@example.com')
            admin_password = app.config.get('ADMIN_PASSWORD', 'change-in-production')
            
            admin_user = User(
                username=admin_username,
                email=admin_email,
                is_admin=True
            )
            admin_user.set_password(admin_password)
            
            try:
                db.session.add(admin_user)
                db.session.commit()
                print(f"Admin user created successfully with username: {admin_username}")
            except Exception as e:
                db.session.rollback()
                print(f"Error creating admin user: {e}")

if __name__ == '__main__':
    check_admin_user()