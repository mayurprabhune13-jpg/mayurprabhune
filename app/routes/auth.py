from flask import Blueprint, render_template, flash, redirect, url_for, request
from urllib.parse import urljoin, urlsplit
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            if next_page:
                target = urljoin(request.host_url, next_page)
                if urlsplit(target).netloc == urlsplit(request.host_url).netloc:
                    return redirect(target)
            return redirect(url_for('admin.dashboard'))
        
        flash('Invalid email or password', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.index'))
