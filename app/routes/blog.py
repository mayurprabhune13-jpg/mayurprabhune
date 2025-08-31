from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models import Post
from app import db
from app.utils import generate_slug

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    """Blog listing page"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category')
    
    query = Post.query.filter_by(status='published')
    
    if category:
        query = query.filter_by(category=category)
        
    posts = query.order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=9, error_out=False)
        
    # Get all unique categories
    categories = db.session.query(Post.category)\
        .filter(Post.category.isnot(None), Post.status=='published')\
        .distinct().all()
    
    return render_template('blog/index.html',
                         posts=posts,
                         categories=categories,
                         current_category=category)

@bp.route('/<slug>')
def post_detail(slug):
    """Blog post detail page"""
    post = Post.query.filter_by(slug=slug, status='published').first_or_404()
    
    # Increment view count
    post.views += 1
    db.session.commit()
    
    return render_template('blog/post_detail.html', post=post)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create new blog post"""
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        category = request.form.get('category')
        status = request.form.get('status', 'draft')
        
        if not title or not content:
            flash('Title and content are required', 'error')
            return redirect(url_for('blog.create_post'))
            
        post = Post(
            title=title,
            slug=generate_slug(title),
            content=content,
            excerpt=excerpt,
            category=category,
            status=status,
            author_id=current_user.id
        )
        
        try:
            db.session.add(post)
            db.session.commit()
            flash('Post created successfully', 'success')
            return redirect(url_for('blog.post_detail', slug=post.slug))
        except:
            db.session.rollback()
            flash('Error creating post', 'error')
            
    return render_template('blog/create_post.html')

@bp.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(slug):
    """Edit blog post"""
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    if post.author_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to edit this post', 'error')
        return redirect(url_for('blog.post_detail', slug=slug))
        
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        excerpt = request.form.get('excerpt')
        category = request.form.get('category')
        status = request.form.get('status')
        
        if not title or not content:
            flash('Title and content are required', 'error')
            return redirect(url_for('blog.edit_post', slug=slug))
            
        post.title = title
        post.slug = generate_slug(title)
        post.content = content
        post.excerpt = excerpt
        post.category = category
        post.status = status
        
        try:
            db.session.commit()
            flash('Post updated successfully', 'success')
            return redirect(url_for('blog.post_detail', slug=post.slug))
        except:
            db.session.rollback()
            flash('Error updating post', 'error')
            
    return render_template('blog/edit_post.html', post=post)

@bp.route('/<slug>/delete')
@login_required
def delete_post(slug):
    """Delete blog post"""
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    if post.author_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to delete this post', 'error')
        return redirect(url_for('blog.post_detail', slug=slug))
        
    try:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully', 'success')
    except:
        db.session.rollback()
        flash('Error deleting post', 'error')
        
    return redirect(url_for('blog.index'))