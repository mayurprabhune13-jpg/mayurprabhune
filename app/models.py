from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500))
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(100))
    status = db.Column(db.String(20), default='draft')  # draft, published
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Post {self.title}>'

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100))
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    rating = db.Column(db.Integer)  # 1-5 rating
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Testimonial by {self.author}>'

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    thumbnail_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(100))
    status = db.Column(db.String(20), default='draft')  # draft, published
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Video {self.title}>'

class SocialPost(db.Model):
    """A cached public post fetched through an authorized platform API."""
    __tablename__ = 'social_post'

    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(20), nullable=False)
    external_id = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.Text)
    permalink = db.Column(db.String(1000), nullable=False)
    media_type = db.Column(db.String(40))
    media_product_type = db.Column(db.String(40))
    media_url = db.Column(db.String(2048))
    thumbnail_url = db.Column(db.String(2048))
    published_at = db.Column(db.DateTime, nullable=False, index=True)
    synced_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_visible = db.Column(db.Boolean, nullable=False, default=True)

    __table_args__ = (
        db.UniqueConstraint('platform', 'external_id', name='uq_social_post_platform_external_id'),
        db.Index('ix_social_post_platform_published_at', 'platform', 'published_at'),
    )

    @property
    def title(self):
        if self.caption:
            first_line = self.caption.strip().splitlines()[0].strip()
            if first_line:
                return first_line[:120]
        return 'LinkedIn post' if self.platform == 'linkedin' else 'Instagram post'

    @property
    def excerpt(self):
        return (self.caption or '').strip()

    @property
    def url(self):
        return self.permalink

    def __repr__(self):
        return f'<SocialPost {self.platform}:{self.external_id}>'

class SiteSettings(db.Model):
    """Editable site identity, default SEO, and homepage presentation settings."""
    __tablename__ = 'site_settings'

    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(120), nullable=False, default='Mayur Prabhune')
    brand_tagline = db.Column(db.String(180), nullable=False, default='AI · LEARNING · ENABLEMENT')
    seo_title = db.Column(db.String(180), nullable=False, default='AI, Learning & Sales Enablement')
    seo_description = db.Column(db.String(320), nullable=False, default='Practical AI learning, workforce capability, and sales enablement with Mayur Prabhune.')
    homepage_eyebrow = db.Column(db.String(180), nullable=False, default='AI / Learning / Enablement')
    homepage_headline = db.Column(db.String(220), nullable=False, default='Building Human Potential in the Age of AI.')
    homepage_support = db.Column(db.String(240), nullable=False, default='Generative AI · Learning Innovation · Retail & Sales Enablement')
    homepage_intro = db.Column(db.Text, nullable=False, default='I help people and teams connect new technology and learning with the work they do every day—from exploring AI to strengthening customer conversations.')
    homepage_photo_url = db.Column(db.String(500))
    featured_video_title = db.Column(db.String(200), nullable=False, default='Featured talk on AI leadership')
    featured_video_description = db.Column(db.String(500), nullable=False, default='Get a glimpse into the world of AI leadership with this featured talk.')
    featured_video_url = db.Column(db.String(500), nullable=False, default='https://www.youtube.com/watch?v=f_Px9x503N0')
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<SiteSettings>'

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='unread')  # unread, read, archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)
    responded = db.Column(db.Boolean, default=False)
    response_sent_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Contact from {self.name}>'

class CaseStudy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    client = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    challenge = db.Column(db.Text)
    solution = db.Column(db.Text)
    results = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    status = db.Column(db.String(20), default='draft')  # draft, published
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<CaseStudy {self.title}>'

class ClientLogo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    logo_url = db.Column(db.String(500), nullable=False)
    website_url = db.Column(db.String(500))
    description = db.Column(db.Text)
    display_order = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ClientLogo {self.client_name}>'
