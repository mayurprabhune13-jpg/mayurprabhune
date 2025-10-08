from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from app.models import Post, Testimonial, Video, Contact, CaseStudy
from app.utils import is_valid_email, format_datetime, reading_time, send_email
from app import db
from app.monitoring import log_function_call, log_db_query
from app.linkedin_integration import get_linkedin_blog_content

bp = Blueprint('main', __name__)

@bp.route('/')
@log_function_call
def index():
    """Home page route"""
    # Initialize empty defaults
    videos = []
    testimonials = []
    posts = []
    case_studies = []
    
    try:
        # Get recent published videos
        videos = Video.query.filter_by(status='published')\
            .order_by(Video.created_at.desc()).limit(6).all()
    except Exception as e:
        current_app.logger.warning(f"Could not fetch videos: {str(e)}")
    
    try:
        # Get approved testimonials
        testimonials = Testimonial.query.filter_by(status='approved')\
            .order_by(Testimonial.created_at.desc()).limit(3).all()
    except Exception as e:
        current_app.logger.warning(f"Could not fetch testimonials: {str(e)}")
    
    try:
        # Get recent published blog posts
        posts = Post.query.filter_by(status='published')\
            .order_by(Post.created_at.desc()).limit(2).all()
    except Exception as e:
        current_app.logger.warning(f"Could not fetch posts: {str(e)}")
    
    # Get LinkedIn blog content
    linkedin_posts = get_linkedin_blog_content(limit=1)
    
    # Combine database posts with LinkedIn content
    all_posts = list(posts) + linkedin_posts
    
    try:
        # Get featured case studies
        case_studies = CaseStudy.query.filter_by(status='published')\
            .order_by(CaseStudy.created_at.desc()).limit(2).all()
    except Exception as e:
        current_app.logger.warning(f"Could not fetch case studies: {str(e)}")
    
    return render_template('index.html',
                         videos=videos,
                         testimonials=testimonials,
                         posts=all_posts,
                         case_studies=case_studies)

@bp.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@bp.route('/services')
def services():
    """Services page route"""
    return render_template('services.html')

@bp.route('/contact', methods=['GET', 'POST'])
@log_function_call
def contact():
    """Contact page route"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if not all([name, email, message]):
            flash('Please fill out all fields', 'error')
            return redirect(url_for('main.contact'))
            
        if not is_valid_email(email):
            flash('Please enter a valid email address', 'error')
            return redirect(url_for('main.contact'))
        
        # Create new contact message
        contact = Contact(
            name=name,
            email=email,
            message=message,
            status='unread'
        )
        
        try:
            db.session.add(contact)
            db.session.commit()
            
            # Send confirmation email to the sender
            confirmation_subject = "Thank you for contacting Mayur Prabhune"
            confirmation_body = f"""
Dear {name},

Thank you for reaching out. I have received your message and will get back to you soon.

Best regards,
Mayur Prabhune
"""
            send_email(
                subject=confirmation_subject,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[email],
                text_body=confirmation_body
            )
            
            # Send notification email to admin
            admin_subject = "New Contact Form Submission"
            admin_body = f"""
New contact form submission received:

Name: {name}
Email: {email}
Message:
{message}
"""
            send_email(
                subject=admin_subject,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[current_app.config['ADMIN_EMAIL']],
                text_body=admin_body
            )
            
            flash('Your message has been sent!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error in contact form: {str(e)}")
            flash('An error occurred. Please try again.', 'error')
            
    return render_template('contact.html',
                         CONTACT_EMAIL='info@mayurprabhune.in',
                         CONTACT_PHONE='+91-7620065818',
                         CONTACT_LINKEDIN='https://www.linkedin.com/in/mayur-prabhune')

@bp.route('/videos')
def videos():
    """Videos listing page"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category')
    
    videos = None
    categories = []
    
    try:
        query = Video.query.filter_by(status='published')
        
        if category:
            query = query.filter_by(category=category)
            
        videos = query.order_by(Video.created_at.desc())\
            .paginate(page=page, per_page=12, error_out=False)
            
        # Get all unique categories for filter
        categories = db.session.query(Video.category)\
            .filter(Video.category.isnot(None), Video.status=='published')\
            .distinct().all()
    except Exception as e:
        current_app.logger.warning(f"Could not fetch videos: {str(e)}")
        # Create empty pagination object
        from flask_sqlalchemy import Pagination
        videos = Pagination(page=page, per_page=12, total=0, items=[])
    
    return render_template('videos.html',
                         videos=videos,
                         categories=categories,
                         current_category=category)

@bp.route('/video/<slug>')
@log_function_call
def video_detail(slug):
    """Video detail page"""
    video = Video.query.filter_by(slug=slug, status='published').first_or_404()
    
    # Increment view count
    video.views += 1
    db.session.commit()
    
    return render_template('video_detail.html', video=video)

@bp.route('/testimonials')
def testimonials():
    """Testimonials page"""
    testimonials = []
    try:
        testimonials = Testimonial.query.filter_by(status='approved')\
            .order_by(Testimonial.created_at.desc()).all()
    except Exception as e:
        current_app.logger.warning(f"Could not fetch testimonials: {str(e)}")
    
    return render_template('testimonials.html', testimonials=testimonials)

@bp.route('/blog')
def blog():
    """Blog listing page"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category')
    
    posts = None
    categories = []
    linkedin_posts = []
    
    try:
        query = Post.query.filter_by(status='published')
        
        if category:
            query = query.filter_by(category=category)
            
        posts = query.order_by(Post.created_at.desc())\
            .paginate(page=page, per_page=6, error_out=False)
            
        # Get all unique categories for filter
        categories = db.session.query(Post.category)\
            .filter(Post.category.isnot(None), Post.status=='published')\
            .distinct().all()

        # Get LinkedIn blog content (only for first page and no category filter)
        if page == 1 and not category:
            try:
                linkedin_posts = get_linkedin_blog_content(limit=3)
            except Exception as e:
                current_app.logger.warning(f"Could not fetch LinkedIn posts: {str(e)}")
                linkedin_posts = []

    except Exception as e:
        current_app.logger.warning(f"Could not fetch posts: {str(e)}")
        # Create empty pagination object
        from flask_sqlalchemy import Pagination
        posts = Pagination(page=page, per_page=6, total=0, items=[])
    
    return render_template('blog.html',
                         posts=posts,
                         linkedin_posts=linkedin_posts,
                         categories=categories,
                         current_category=category)

@bp.route('/blog/<slug>')
@log_function_call
def post_detail(slug):
    """Blog post detail page"""
    post = Post.query.filter_by(slug=slug, status='published').first_or_404()
    
    # Increment view count
    post.views += 1
    db.session.commit()
    
    # Calculate reading time
    post.reading_time = reading_time(post.content)
    
    return render_template('post_detail.html', post=post)

@bp.route('/success-stories')
def success_stories():
    """Case studies listing page"""
    page = request.args.get('page', 1, type=int)
    industry = request.args.get('industry')
    
    case_studies = None
    industries = []
    
    try:
        query = CaseStudy.query.filter_by(status='published')
        
        if industry:
            query = query.filter_by(industry=industry)
            
        case_studies = query.order_by(CaseStudy.created_at.desc())\
            .paginate(page=page, per_page=6, error_out=False)
            
        # Get all unique industries for filter
        industries = db.session.query(CaseStudy.industry)\
            .filter(CaseStudy.status=='published')\
            .distinct().all()
    except Exception as e:
        current_app.logger.warning(f"Could not fetch case studies: {str(e)}")
        # Create empty pagination object
        from flask_sqlalchemy import Pagination
        case_studies = Pagination(page=page, per_page=6, total=0, items=[])
    
    return render_template('success_stories.html',
                         case_studies=case_studies,
                         industries=industries,
                         current_industry=industry)

@bp.route('/success-stories/<slug>')
@log_function_call
def case_study_detail(slug):
    """Case study detail page"""
    case_study = CaseStudy.query.filter_by(slug=slug, status='published').first_or_404()
    return render_template('case_study_detail.html', case_study=case_study)

# Template filters
@bp.app_template_filter('datetime')
def _jinja2_filter_datetime(date):
    """Format datetime for templates"""
    return format_datetime(date)

# Error handlers
@bp.app_errorhandler(404)
@log_function_call
def not_found_error(error):
    return render_template('errors/404.html'), 404

@bp.app_errorhandler(500)
@log_function_call
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500