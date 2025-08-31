from app import create_app, db
from app.models import User, Post, Testimonial, Video, Contact, CaseStudy

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Provide context for Flask shell"""
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'Testimonial': Testimonial,
        'Video': Video,
        'Contact': Contact,
        'CaseStudy': CaseStudy
    }

if __name__ == '__main__':
    app.run(debug=True)