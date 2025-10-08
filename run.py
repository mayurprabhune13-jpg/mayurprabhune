from app import app, db
from app.models import User
from werkzeug.security import generate_password_hash

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            admin = User(
                email='admin@example.com',
                password_hash=generate_password_hash('AdminPass123!'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully")
        else:
            print("Admin user already exists")
            
        print("Database setup completed")
        
    app.run(debug=True)