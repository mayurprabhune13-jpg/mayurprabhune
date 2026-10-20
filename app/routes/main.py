from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, Response
from urllib.parse import urlsplit
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import case
from app.models import Post, Testimonial, Video, Contact, CaseStudy, ClientLogo, SocialPost
from app.utils import is_valid_email, format_datetime, reading_time, send_email
from app import db
from app.monitoring import log_function_call, log_db_query
from app.site_settings import get_site_settings

bp = Blueprint('main', __name__)

FEATURED_VIDEO = {
    'embed_url': 'https://www.youtube-nocookie.com/embed/f_Px9x503N0?rel=0',
    'watch_url': 'https://www.youtube.com/watch?v=f_Px9x503N0',
    'title': 'Featured talk on AI leadership',
    'description': 'Get a glimpse into the world of AI leadership with this featured talk.'
}


def get_recent_social_posts(platform=None, limit=3):
    try:
        query = SocialPost.query.filter_by(is_visible=True)
        if platform:
            query = query.filter_by(platform=platform)
        curated_first = case((SocialPost.external_id.like('manual:%'), 0), else_=1)
        return query.order_by(curated_first, SocialPost.published_at.desc()).limit(limit).all()
    except Exception as error:
        db.session.rollback()
        current_app.logger.warning('Could not load cached social feed (%s).', type(error).__name__)
        return []

@bp.app_template_filter('media_url')
def media_url(value):
    """Resolve stored upload paths and allow only HTTPS remote media URLs."""
    if not value:
        return ''
    value = str(value).strip()
    parsed = urlsplit(value)
    if parsed.scheme == 'https' and parsed.netloc:
        return value
    if value.startswith('/static/'):
        return value
    return url_for('static', filename=value.lstrip('/'))

@bp.route('/')
@log_function_call
def index():
    """Home page route"""
    # Initialize empty defaults
    videos = []
    testimonials = []
    posts = []
    case_studies = []
    client_logos = []
    
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
    
    try:
        # Get featured case studies
        case_studies = CaseStudy.query.filter_by(status='published')\
            .order_by(CaseStudy.created_at.desc()).limit(2).all()
    except Exception as e:
        current_app.logger.warning(f"Could not fetch case studies: {str(e)}")

    try:
        client_logos = ClientLogo.query.filter_by(status='active')\
            .order_by(ClientLogo.display_order.asc(), ClientLogo.created_at.desc()).limit(12).all()
    except Exception as e:
        current_app.logger.warning(f"Could not fetch client logos: {str(e)}")

    linkedin_posts = get_recent_social_posts('linkedin', 3)
    instagram_posts = get_recent_social_posts('instagram', 3)
    
    settings = get_site_settings()
    video_url = settings.featured_video_url or FEATURED_VIDEO['watch_url']
    parsed_video = urlsplit(video_url)
    video_id = parsed_video.path.rstrip('/').split('/')[-1] if parsed_video.netloc in ('youtu.be', 'www.youtu.be') else None
    if parsed_video.netloc.endswith('youtube.com'):
        from urllib.parse import parse_qs
        video_id = parse_qs(parsed_video.query).get('v', [None])[0]
        if not video_id:
            path_parts = [part for part in parsed_video.path.split('/') if part]
            if len(path_parts) > 1 and path_parts[0] in ('embed', 'shorts', 'live'):
                video_id = path_parts[1]
    featured_video = {
        'embed_url': f'https://www.youtube-nocookie.com/embed/{video_id}?rel=0' if video_id else FEATURED_VIDEO['embed_url'],
        'watch_url': video_url,
        'title': settings.featured_video_title,
        'description': settings.featured_video_description,
    }

    return render_template('index.html',
                         videos=videos,
                         testimonials=testimonials,
                         posts=posts,
                         case_studies=case_studies,
                         client_logos=client_logos,
                         featured_video=featured_video,
                         linkedin_posts=linkedin_posts,
                         instagram_posts=instagram_posts)

@bp.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@bp.route('/services')
def services():
    """Services page route"""
    return render_template('services.html')

@bp.route('/premium-product-sales-training')
def premium_product_sales_training():
    """Focused page for premium product sales training enquiries."""
    return render_template('premium_product_sales_training.html')

@bp.route('/contact', methods=['GET', 'POST'])
@log_function_call
def contact():
    """Contact page route"""
    if request.method == 'POST':
        # Quietly accept bot submissions into a neutral success path without storing them.
        if request.form.get('website', '').strip():
            flash('Thanks for reaching out. Your message has been received.', 'success')
            return redirect(url_for('main.contact'))

        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        topic = request.form.get('topic', '').strip()
        
        if not all([name, email, message]):
            flash('Please complete your name, email, and message.', 'error')
            return redirect(url_for('main.contact'))

        if len(name) > 100 or len(email) > 120 or len(message) > 5000:
            flash('Please shorten your name, email, or message and try again.', 'error')
            return redirect(url_for('main.contact'))
            
        if not is_valid_email(email):
            flash('Please enter a valid email address', 'error')
            return redirect(url_for('main.contact'))

        topic_labels = {
            'ai-training': 'AI training',
            'premium-product-sales-training': 'Premium product sales training',
            'other': 'Other enquiry'
        }
        topic_label = topic_labels.get(topic)
        if topic_label:
            message = f"Program interest: {topic_label}\n\n{message}"
        
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
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Could not save contact form submission: {str(e)}")
            flash('We could not save your message. Please try again.', 'error')
            return redirect(url_for('main.contact'))

        confirmation_subject = "Thank you for contacting Mayur Prabhune"
        confirmation_body = f"""
Dear {name},

Thank you for reaching out. I have received your message and will get back to you soon.

Best regards,
Mayur Prabhune
"""
        try:
            send_email(
                subject=confirmation_subject,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[email],
                text_body=confirmation_body
            )
        except Exception as e:
            current_app.logger.warning(f"Could not send contact confirmation email: {str(e)}")

        admin_subject = "New Contact Form Submission"
        admin_body = f"""
New contact form submission received:

Name: {name}
Email: {email}
Message:
{message}
"""
        try:
            send_email(
                subject=admin_subject,
                sender=current_app.config['MAIL_DEFAULT_SENDER'],
                recipients=[current_app.config['ADMIN_EMAIL']],
                text_body=admin_body
            )
        except Exception as e:
            current_app.logger.warning(f"Could not send contact notification email: {str(e)}")

        flash('Your message has been received. Thank you for reaching out.', 'success')
        return redirect(url_for('main.contact'))
            
    return render_template('contact.html',
                         CONTACT_EMAIL='info@mayurprabhune.in',
                         CONTACT_PHONE='+91-7620065818',
                         CONTACT_LINKEDIN='https://www.linkedin.com/in/mayur-prabhune')

@bp.route('/robots.txt')
def robots_txt():
    site_url = (current_app.config.get('SITE_URL') or 'https://mayurprabhune.in').rstrip('/')
    sitemap_url = f"{site_url}{url_for('main.sitemap_xml')}"
    return Response(f"User-agent: *\nAllow: /\nSitemap: {sitemap_url}\n", mimetype='text/plain')

@bp.route('/sitemap.xml')
def sitemap_xml():
    site_url = (current_app.config.get('SITE_URL') or 'https://mayurprabhune.in').rstrip('/')
    static_endpoints = [
        'main.index', 'main.about', 'main.services',
        'main.premium_product_sales_training', 'main.contact',
        'main.videos', 'main.testimonials', 'main.blog', 'main.success_stories'
    ]
    urls = [{'loc': f"{site_url}{url_for(endpoint)}", 'lastmod': None} for endpoint in static_endpoints]

    try:
        for post in Post.query.filter_by(status='published').all():
            urls.append({'loc': f"{site_url}{url_for('main.post_detail', slug=post.slug)}", 'lastmod': post.updated_at})
        for video in Video.query.filter_by(status='published').all():
            urls.append({'loc': f"{site_url}{url_for('main.video_detail', slug=video.slug)}", 'lastmod': video.created_at})
        for case_study in CaseStudy.query.filter_by(status='published').all():
            urls.append({'loc': f"{site_url}{url_for('main.case_study_detail', slug=case_study.slug)}", 'lastmod': case_study.created_at})
    except Exception as e:
        current_app.logger.warning(f"Could not include all published content in sitemap: {str(e)}")

    return render_template('sitemap.xml', urls=urls), 200, {'Content-Type': 'application/xml; charset=utf-8'}

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
                         current_category=category,
                         featured_video=FEATURED_VIDEO)

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

    except Exception as e:
        current_app.logger.warning(f"Could not fetch posts: {str(e)}")
        # Create empty pagination object for posts
        posts = Pagination(None, page=page, per_page=6, total=0, items=[])
    
    return render_template('blog.html',
                         posts=posts,
                         linkedin_posts=get_recent_social_posts('linkedin', 3),
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
        # Create empty pagination object for case studies
        case_studies = Pagination(None, page=page, per_page=6, total=0, items=[])
    
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
