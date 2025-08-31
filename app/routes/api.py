from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models import Video, Testimonial, Contact, Post, CaseStudy
from app.utils import is_valid_email
from datetime import datetime

bp = Blueprint('api', __name__)

@bp.before_request
@login_required
def require_admin():
    """Ensure only admin users can access API endpoints"""
    if not current_user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

def serialize_video(video):
    """Serialize video object to dict"""
    return {
        'id': video.id,
        'title': video.title,
        'slug': video.slug,
        'description': video.description,
        'thumbnail_url': video.thumbnail_url,
        'video_url': video.video_url,
        'category': video.category,
        'status': video.status,
        'views': video.views,
        'created_at': video.created_at.isoformat(),
        'published_at': video.published_at.isoformat() if video.published_at else None
    }

def serialize_post(post):
    """Serialize blog post object to dict"""
    return {
        'id': post.id,
        'title': post.title,
        'slug': post.slug,
        'content': post.content,
        'excerpt': post.excerpt,
        'image_url': post.image_url,
        'category': post.category,
        'status': post.status,
        'views': post.views,
        'author': {
            'id': post.author.id,
            'username': post.author.username
        },
        'created_at': post.created_at.isoformat(),
        'updated_at': post.updated_at.isoformat(),
        'published_at': post.published_at.isoformat() if post.published_at else None
    }

def serialize_case_study(case_study):
    """Serialize case study object to dict"""
    return {
        'id': case_study.id,
        'title': case_study.title,
        'slug': case_study.slug,
        'client': case_study.client,
        'industry': case_study.industry,
        'description': case_study.description,
        'challenge': case_study.challenge,
        'solution': case_study.solution,
        'results': case_study.results,
        'image_url': case_study.image_url,
        'status': case_study.status,
        'created_at': case_study.created_at.isoformat(),
        'published_at': case_study.published_at.isoformat() if case_study.published_at else None
    }

@bp.route('/videos', methods=['GET'])
def get_videos():
    """Get all videos with optional filtering"""
    status = request.args.get('status', 'published')
    category = request.args.get('category')
    
    query = Video.query
    
    if status != 'all':
        query = query.filter_by(status=status)
    if category:
        query = query.filter_by(category=category)
        
    videos = query.order_by(Video.created_at.desc()).all()
    return jsonify([serialize_video(v) for v in videos])

@bp.route('/video/<int:id>', methods=['GET'])
def get_video(id):
    """Get a specific video"""
    video = Video.query.get_or_404(id)
    return jsonify(serialize_video(video))

@bp.route('/posts', methods=['GET'])
def get_posts():
    """Get all blog posts with optional filtering"""
    status = request.args.get('status', 'published')
    category = request.args.get('category')
    
    query = Post.query
    
    if status != 'all':
        query = query.filter_by(status=status)
    if category:
        query = query.filter_by(category=category)
        
    posts = query.order_by(Post.created_at.desc()).all()
    return jsonify([serialize_post(p) for p in posts])

@bp.route('/post/<int:id>', methods=['GET'])
def get_post(id):
    """Get a specific blog post"""
    post = Post.query.get_or_404(id)
    return jsonify(serialize_post(post))

@bp.route('/case-studies', methods=['GET'])
def get_case_studies():
    """Get all case studies with optional filtering"""
    status = request.args.get('status', 'published')
    industry = request.args.get('industry')
    
    query = CaseStudy.query
    
    if status != 'all':
        query = query.filter_by(status=status)
    if industry:
        query = query.filter_by(industry=industry)
        
    case_studies = query.order_by(CaseStudy.created_at.desc()).all()
    return jsonify([serialize_case_study(cs) for cs in case_studies])

@bp.route('/case-study/<int:id>', methods=['GET'])
def get_case_study(id):
    """Get a specific case study"""
    case_study = CaseStudy.query.get_or_404(id)
    return jsonify(serialize_case_study(case_study))

@bp.route('/testimonials', methods=['GET'])
def get_testimonials():
    """Get all testimonials with optional filtering"""
    status = request.args.get('status', 'approved')
    
    query = Testimonial.query
    
    if status != 'all':
        query = query.filter_by(status=status)
        
    testimonials = query.order_by(Testimonial.created_at.desc()).all()
    return jsonify([{
        'id': t.id,
        'author': t.author,
        'role': t.role,
        'content': t.content,
        'image_url': t.image_url,
        'rating': t.rating,
        'status': t.status,
        'created_at': t.created_at.isoformat(),
        'approved_at': t.approved_at.isoformat() if t.approved_at else None
    } for t in testimonials])

@bp.route('/contact', methods=['POST'])
def create_contact():
    """Create a new contact message"""
    data = request.get_json()
    
    if not all(k in data for k in ('name', 'email', 'message')):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if not is_valid_email(data['email']):
        return jsonify({'error': 'Invalid email address'}), 400
        
    contact = Contact(
        name=data['name'],
        email=data['email'],
        message=data['message'],
        status='unread'
    )
    
    try:
        db.session.add(contact)
        db.session.commit()
        return jsonify({
            'id': contact.id,
            'name': contact.name,
            'email': contact.email,
            'message': contact.message,
            'status': contact.status,
            'created_at': contact.created_at.isoformat()
        }), 201
    except:
        db.session.rollback()
        return jsonify({'error': 'Error creating contact message'}), 500

@bp.route('/messages', methods=['GET'])
def get_messages():
    """Get messages with optional status filter"""
    status = request.args.get('status', 'unread')
    
    query = Contact.query
    
    if status != 'all':
        query = query.filter_by(status=status)
        
    messages = query.order_by(Contact.created_at.desc()).all()
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'email': m.email,
        'message': m.message,
        'status': m.status,
        'created_at': m.created_at.isoformat(),
        'read_at': m.read_at.isoformat() if m.read_at else None,
        'responded': m.responded,
        'response_sent_at': m.response_sent_at.isoformat() if m.response_sent_at else None
    } for m in messages])

@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    return jsonify({
        'videos': {
            'total': Video.query.count(),
            'published': Video.query.filter_by(status='published').count(),
            'draft': Video.query.filter_by(status='draft').count()
        },
        'posts': {
            'total': Post.query.count(),
            'published': Post.query.filter_by(status='published').count(),
            'draft': Post.query.filter_by(status='draft').count()
        },
        'case_studies': {
            'total': CaseStudy.query.count(),
            'published': CaseStudy.query.filter_by(status='published').count(),
            'draft': CaseStudy.query.filter_by(status='draft').count()
        },
        'testimonials': {
            'total': Testimonial.query.count(),
            'approved': Testimonial.query.filter_by(status='approved').count(),
            'pending': Testimonial.query.filter_by(status='pending').count(),
            'rejected': Testimonial.query.filter_by(status='rejected').count()
        },
        'messages': {
            'total': Contact.query.count(),
            'unread': Contact.query.filter_by(status='unread').count(),
            'read': Contact.query.filter_by(status='read').count(),
            'archived': Contact.query.filter_by(status='archived').count()
        }
    })

# Error handlers
@bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500