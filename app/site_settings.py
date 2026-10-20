"""Shared defaults and safe access for editable site settings."""
from types import SimpleNamespace

from flask import current_app

from app import db
from app.models import SiteSettings


DEFAULTS = {
    'site_name': 'Mayur Prabhune',
    'brand_tagline': 'AI · LEARNING · ENABLEMENT',
    'seo_title': 'AI, Learning & Sales Enablement',
    'seo_description': 'Practical AI learning, workforce capability, and sales enablement with Mayur Prabhune.',
    'homepage_eyebrow': 'AI / Learning / Enablement',
    'homepage_headline': 'Building Human Potential in the Age of AI.',
    'homepage_support': 'Generative AI · Learning Innovation · Retail & Sales Enablement',
    'homepage_intro': 'I help people and teams connect new technology and learning with the work they do every day—from exploring AI to strengthening customer conversations.',
    'homepage_photo_url': '',
    'featured_video_title': 'Featured talk on AI leadership',
    'featured_video_description': 'Get a glimpse into the world of AI leadership with this featured talk.',
    'featured_video_url': 'https://www.youtube.com/watch?v=f_Px9x503N0',
}


def get_site_settings():
    """Return saved settings or safe defaults if setup/migration is pending."""
    try:
        saved = SiteSettings.query.first()
        if saved:
            return saved
    except Exception as error:
        db.session.rollback()
        current_app.logger.warning('Could not load site settings (%s).', type(error).__name__)
    return SimpleNamespace(**DEFAULTS)
