from app import create_app, db
from app.models import Video, Testimonial, Post, CaseStudy, User
from datetime import datetime, timedelta
import random

app = create_app()

def create_sample_data():
    """Create sample data for testing"""
    
    # Create admin user if not exists
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin_user.set_password('adminpass123')
        db.session.add(admin_user)
    
    # Sample videos
    video_categories = ['AI Leadership', 'Machine Learning', 'Data Science', 'Business Strategy']
    videos = [
        Video(
            title='Introduction to AI Leadership',
            slug='introduction-to-ai-leadership',
            description='Learn the fundamentals of leading AI initiatives in your organization.',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            category=random.choice(video_categories),
            status='published',
            views=random.randint(100, 1000),
            created_at=datetime.now() - timedelta(days=random.randint(1, 30))
        ),
        Video(
            title='Ethical AI Implementation',
            slug='ethical-ai-implementation',
            description='Best practices for implementing AI ethically in business environments.',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            category=random.choice(video_categories),
            status='published',
            views=random.randint(100, 1000),
            created_at=datetime.now() - timedelta(days=random.randint(1, 30))
        ),
        Video(
            title='AI Strategy for Executives',
            slug='ai-strategy-for-executives',
            description='A comprehensive guide for executives to develop effective AI strategies.',
            video_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            category=random.choice(video_categories),
            status='published',
            views=random.randint(100, 1000),
            created_at=datetime.now() - timedelta(days=random.randint(1, 30))
        )
    ]
    
    # Sample testimonials
    testimonials = [
        Testimonial(
            author='Jane Doe',
            role='CEO, Tech Innovations Inc.',
            content="Mayur's guidance was a game-changer for our AI strategy. His deep expertise and practical approach helped us navigate the complexities of AI with confidence and clarity.",
            status='approved',
            created_at=datetime.now() - timedelta(days=10)
        ),
        Testimonial(
            author='John Smith',
            role='CTO, Future Solutions',
            content="The workshop on AI for Product Managers was incredibly insightful. Mayur has a unique ability to break down complex topics into actionable insights.",
            status='approved',
            created_at=datetime.now() - timedelta(days=5)
        ),
        Testimonial(
            author='Samantha Lee',
            role='Director, Global Enterprises',
            content="Working with Mayur helped us build a strong, ethical framework for our AI initiatives. His consulting was invaluable for our long-term vision.",
            status='approved',
            created_at=datetime.now() - timedelta(days=3)
        )
    ]
    
    # Sample blog posts
    posts = [
        Post(
            title='The 5 Pillars of a Successful AI Strategy',
            slug='5-pillars-successful-ai-strategy',
            excerpt='Discover the key components that every leader needs to consider when building a robust AI roadmap for their organization.',
            content='Full content about AI strategy pillars...',
            category='AI Leadership',
            status='published',
            views=random.randint(50, 500),
            author_id=admin_user.id,
            created_at=datetime.now() - timedelta(days=15)
        ),
        Post(
            title='Ethical AI: A Leader\'s Responsibility',
            slug='ethical-ai-leaders-responsibility',
            excerpt='Navigating the ethical landscape of AI is crucial. Learn how to lead with integrity and build trust in your AI initiatives.',
            content='Full content about ethical AI...',
            category='Ethics',
            status='published',
            views=random.randint(50, 500),
            author_id=admin_user.id,
            created_at=datetime.now() - timedelta(days=8)
        ),
        Post(
            title='Demystifying AI for the C-Suite',
            slug='demystifying-ai-c-suite',
            excerpt='A practical guide for executives to understand AI\'s potential and limitations, enabling informed decision-making.',
            content='Full content about AI for executives...',
            category='Executive Education',
            status='published',
            views=random.randint(50, 500),
            author_id=admin_user.id,
            created_at=datetime.now() - timedelta(days=2)
        )
    ]
    
    # Sample case studies
    case_studies = [
        CaseStudy(
            title='AI Transformation at FinTech Corp',
            slug='ai-transformation-fintech-corp',
            client='FinTech Corp',
            description='How a financial technology company successfully implemented AI across their operations. Full case study content...',
            challenge='Faced challenges in integrating AI with existing legacy systems and ensuring data privacy compliance.',
            solution='Implemented a phased AI adoption strategy with robust data governance and custom integration solutions.',
            results='Achieved 40% operational efficiency improvement and reduced costs by 25% within the first year.',
            industry='Financial Services',
            status='published',
            created_at=datetime.now() - timedelta(days=20)
        ),
        CaseStudy(
            title='Manufacturing Efficiency with AI',
            slug='manufacturing-efficiency-ai',
            client='Manufacturing Inc',
            description='A manufacturing company achieved 30% efficiency gains through AI-powered optimization. Full case study content...',
            challenge='Struggled with production bottlenecks, quality control issues, and predictive maintenance.',
            solution='Deployed AI-powered predictive maintenance systems and computer vision for quality control.',
            results='30% increase in production efficiency, 50% reduction in downtime, and improved product quality.',
            industry='Manufacturing',
            status='published',
            created_at=datetime.now() - timedelta(days=12)
        )
    ]
    
    # Add all sample data to session
    for video in videos:
        db.session.add(video)
    
    for testimonial in testimonials:
        db.session.add(testimonial)
    
    for post in posts:
        db.session.add(post)
    
    for case_study in case_studies:
        db.session.add(case_study)
    
    try:
        db.session.commit()
        print("Sample data created successfully!")
        print(f"Videos: {len(videos)}")
        print(f"Testimonials: {len(testimonials)}")
        print(f"Posts: {len(posts)}")
        print(f"Case Studies: {len(case_studies)}")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating sample data: {e}")

if __name__ == '__main__':
    with app.app_context():
        create_sample_data()