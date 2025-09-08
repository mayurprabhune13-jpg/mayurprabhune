from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from app import db
from app.models import Video, Testimonial, Post, Contact, CaseStudy
from app import Config
from app.utils import generate_slug

bp = Blueprint('admin', __name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@bp.before_request
@login_required
def require_admin():
    """Ensure only admin users can access admin routes"""
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.index'))

@bp.route('/dashboard')
def dashboard():
    """Admin dashboard showing overview of content"""
    # Calculate total views from all videos
    total_views = db.session.query(db.func.sum(Video.views)).scalar() or 0
    
    stats = {
        'total_videos': Video.query.count(),
        'total_views': total_views,
        'total_testimonials': Testimonial.query.count(),
        'total_messages': Contact.query.count(),
        'unread_messages': Contact.query.filter_by(status='unread').count()
    }
    
    recent_videos = Video.query.order_by(Video.created_at.desc()).limit(5).all()
    recent_testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).limit(5).all()
    recent_messages = Contact.query.filter_by(status='unread')\
        .order_by(Contact.created_at.desc()).limit(5).all()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    
    # Generate dummy chart data for weekly statistics
    chart_data = {
        'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'views': [12, 19, 3, 5, 2, 3, 15],
        'messages': [5, 8, 2, 4, 1, 6, 10]
    }
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_videos=recent_videos,
                         recent_testimonials=recent_testimonials,
                         recent_messages=recent_messages,
                         recent_posts=recent_posts,
                         chart_data=chart_data)

@bp.route('/videos', methods=['GET', 'POST'])
def videos():
    """Manage videos"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        video_url = request.form.get('video_url')
        category = request.form.get('category')
        status = request.form.get('status', 'draft')
        thumbnail = request.files.get('thumbnail')
        
        if not all([title, video_url]):
            flash('Title and video URL are required', 'error')
            return redirect(url_for('admin.videos'))
            
        thumbnail_url = None
        if thumbnail and allowed_file(thumbnail.filename):
            filename = secure_filename(thumbnail.filename)
            thumbnail.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            thumbnail_url = f'/static/uploads/{filename}'
            
        video = Video(
            title=title,
            slug=generate_slug(title),
            description=description,
            video_url=video_url,
            thumbnail_url=thumbnail_url,
            category=category,
            status=status,
            published_at=datetime.utcnow() if status == 'published' else None
        )
        
        try:
            db.session.add(video)
            db.session.commit()
            flash('Video added successfully', 'success')
        except:
            db.session.rollback()
            flash('Error adding video', 'error')
            
        return redirect(url_for('admin.videos'))
        
    videos = Video.query.order_by(Video.created_at.desc()).all()
    return render_template('admin/videos.html', videos=videos)

@bp.route('/testimonials', methods=['GET', 'POST'])
def testimonials():
    """Manage testimonials"""
    if request.method == 'POST':
        author = request.form.get('author')
        role = request.form.get('role')
        content = request.form.get('content')
        rating = request.form.get('rating')
        status = request.form.get('status', 'pending')
        image = request.files.get('image')
        
        if not all([author, content]):
            flash('Author and content are required', 'error')
            return redirect(url_for('admin.testimonials'))
            
        image_url = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            image_url = f'/static/uploads/{filename}'
            
        testimonial = Testimonial(
            author=author,
            role=role,
            content=content,
            rating=rating,
            status=status,
            image_url=image_url,
            approved_at=datetime.utcnow() if status == 'approved' else None
        )
        
        try:
            db.session.add(testimonial)
            db.session.commit()
            flash('Testimonial added successfully', 'success')
        except:
            db.session.rollback()
            flash('Error adding testimonial', 'error')
            
        return redirect(url_for('admin.testimonials'))
        
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials.html', testimonials=testimonials)

@bp.route('/posts', methods=['GET', 'POST'])
def posts():
    """Manage blog posts"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        category = request.form.get('category')
        status = request.form.get('status', 'draft')
        image = request.files.get('image')
        
        if not all([title, content]):
            flash('Title and content are required', 'error')
            return redirect(url_for('admin.posts'))
            
        image_url = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            image_url = f'/static/uploads/{filename}'
            
        post = Post(
            title=title,
            slug=generate_slug(title),
            content=content,
            excerpt=excerpt,
            category=category,
            status=status,
            image_url=image_url,
            author_id=current_user.id,
            published_at=datetime.utcnow() if status == 'published' else None
        )
        
        try:
            db.session.add(post)
            db.session.commit()
            flash('Post added successfully', 'success')
        except:
            db.session.rollback()
            flash('Error adding post', 'error')
            
        return redirect(url_for('admin.posts'))
        
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/posts.html', posts=posts)

@bp.route('/case-studies', methods=['GET', 'POST'])
def case_studies():
    """Manage case studies"""
    if request.method == 'POST':
        title = request.form.get('title')
        client = request.form.get('client')
        industry = request.form.get('industry')
        description = request.form.get('description')
        challenge = request.form.get('challenge')
        solution = request.form.get('solution')
        results = request.form.get('results')
        status = request.form.get('status', 'draft')
        image = request.files.get('image')
        
        if not all([title, client, industry, description]):
            flash('Title, client, industry and description are required', 'error')
            return redirect(url_for('admin.case_studies'))
            
        image_url = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(Config.UPLOAD_FOLDER, filename))
            image_url = f'/static/uploads/{filename}'
            
        case_study = CaseStudy(
            title=title,
            slug=generate_slug(title),
            client=client,
            industry=industry,
            description=description,
            challenge=challenge,
            solution=solution,
            results=results,
            status=status,
            image_url=image_url,
            published_at=datetime.utcnow() if status == 'published' else None
        )
        
        try:
            db.session.add(case_study)
            db.session.commit()
            flash('Case study added successfully', 'success')
        except:
            db.session.rollback()
            flash('Error adding case study', 'error')
            
        return redirect(url_for('admin.case_studies'))
        
    case_studies = CaseStudy.query.order_by(CaseStudy.created_at.desc()).all()
    return render_template('admin/case_studies.html', case_studies=case_studies)

@bp.route('/messages')
def messages():
    """View and manage contact messages"""
    messages = Contact.query.order_by(Contact.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)

@bp.route('/message/<int:id>/status/<status>')
def update_message_status(id, status):
    """Update message status"""
    message = Contact.query.get_or_404(id)
    if status not in ['unread', 'read', 'archived']:
        flash('Invalid status', 'error')
        return redirect(url_for('admin.messages'))
        
    message.status = status
    if status == 'read' and not message.read_at:
        message.read_at = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('admin.messages'))

@bp.route('/message/<int:id>/toggle-response')
def toggle_message_response(id):
    """Toggle message responded status"""
    message = Contact.query.get_or_404(id)
    message.responded = not message.responded
    message.response_sent_at = datetime.utcnow() if message.responded else None
    db.session.commit()
    return redirect(url_for('admin.messages'))

def delete_resource(model, id, redirect_endpoint):
    """Generic delete function for any resource"""
    resource = model.query.get_or_404(id)
    try:
        db.session.delete(resource)
        db.session.commit()
        flash(f'{model.__name__} deleted successfully', 'success')
    except:
        db.session.rollback()
        flash(f'Error deleting {model.__name__}', 'error')
    return redirect(url_for(redirect_endpoint))

@bp.route('/video/<int:id>/delete')
def delete_video(id):
    """Delete a video"""
    return delete_resource(Video, id, 'admin.videos')

@bp.route('/testimonial/<int:id>/delete')
def delete_testimonial(id):
    """Delete a testimonial"""
    return delete_resource(Testimonial, id, 'admin.testimonials')

@bp.route('/post/<int:id>/delete')
def delete_post(id):
    """Delete a blog post"""
    return delete_resource(Post, id, 'admin.posts')

@bp.route('/case-study/<int:id>/delete')
def delete_case_study(id):
    """Delete a case study"""
    return delete_resource(CaseStudy, id, 'admin.case_studies')