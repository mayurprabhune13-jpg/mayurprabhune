import re
from unidecode import unidecode
from datetime import datetime
from flask import current_app
from flask_mail import Message
from app import mail

def generate_slug(text):
    """
    Generate a URL-friendly slug from the given text.
    Example: "Hello World!" -> "hello-world"
    """
    # Convert to lowercase and remove accents
    text = unidecode(text.lower())
    
    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    
    return text

def format_datetime(dt):
    """Format datetime for display"""
    if not dt:
        return ''
    return dt.strftime('%B %d, %Y %I:%M %p')

def get_file_extension(filename):
    """Get file extension from filename"""
    if '.' not in filename:
        return ''
    return filename.rsplit('.', 1)[1].lower()

def is_valid_email(email):
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def truncate_text(text, length=100, suffix='...'):
    """Truncate text to specified length"""
    if not text:
        return ''
    if len(text) <= length:
        return text
    return ' '.join(text[:length+1].split(' ')[0:-1]) + suffix

def count_words(text):
    """Count words in text"""
    if not text:
        return 0
    return len(text.split())

def reading_time(text, wpm=200):
    """Calculate reading time in minutes"""
    word_count = count_words(text)
    minutes = word_count / wpm
    return max(1, round(minutes))

def send_email(subject, sender, recipients, text_body, html_body=None):
    """Send an email using Flask-Mail"""
    try:
        msg = Message(subject, sender=sender, recipients=recipients)
        msg.body = text_body
        if html_body:
            msg.html = html_body
        mail.send(msg)
        return True
    except Exception as e:
        current_app.logger.error(f"Error sending email: {str(e)}")
        return False