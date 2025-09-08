from app import create_app, db
from app.models import Video, Testimonial, Post, CaseStudy

app = create_app()

with app.app_context():
    print("Database record counts:")
    print('Video count:', Video.query.count())
    print('Testimonial count:', Testimonial.query.count())
    print('Post count:', Post.query.count())
    print('CaseStudy count:', CaseStudy.query.count())