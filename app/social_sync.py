"""Fetch only the authenticated user's public social content via official APIs."""
from datetime import datetime, timezone
import logging
import os

import requests

from app import db
from app.models import SocialPost

logger = logging.getLogger(__name__)
REQUEST_TIMEOUT = (5, 25)
SOCIAL_FEED_LIMIT = 25


def _utc_datetime(value):
    if isinstance(value, (int, float)):
        # LinkedIn timestamps are Unix milliseconds.
        value = value / 1000 if value > 10_000_000_000 else value
        return datetime.fromtimestamp(value, tz=timezone.utc).replace(tzinfo=None)
    if isinstance(value, str) and value.strip():
        parsed = datetime.fromisoformat(value.strip().replace('Z', '+00:00'))
        if parsed.tzinfo:
            parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
        return parsed
    return None


def _linkedin_posts():
    token = os.environ.get('LINKEDIN_ACCESS_TOKEN', '').strip()
    author_urn = os.environ.get('LINKEDIN_AUTHOR_URN', '').strip()
    if not token or not author_urn:
        return None

    version = os.environ.get('LINKEDIN_API_VERSION', '202610').strip()
    response = requests.get(
        'https://api.linkedin.com/rest/posts',
        headers={
            'Authorization': f'Bearer {token}',
            'Linkedin-Version': version,
            'X-Restli-Protocol-Version': '2.0.0',
            'X-RestLi-Method': 'FINDER',
        },
        params={
            'q': 'author',
            'author': author_urn,
            'count': SOCIAL_FEED_LIMIT,
            'sortBy': 'CREATED',
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    elements = response.json().get('elements', [])
    posts = []
    for item in elements:
        if item.get('lifecycleState') not in (None, 'PUBLISHED'):
            continue
        if item.get('visibility') not in (None, 'PUBLIC'):
            continue
        external_id = str(item.get('id') or '').strip()
        published_at = _utc_datetime(item.get('publishedAt') or item.get('createdAt'))
        if not external_id or not published_at:
            continue
        commentary = item.get('commentary') or ''
        if isinstance(commentary, dict):
            commentary = commentary.get('text') or ''
        permalink_id = external_id
        posts.append({
            'platform': 'linkedin',
            'external_id': external_id,
            'caption': str(commentary)[:10000],
            'permalink': f'https://www.linkedin.com/feed/update/{permalink_id}/',
            'media_type': None,
            'media_product_type': None,
            'media_url': None,
            'thumbnail_url': None,
            'published_at': published_at,
        })
    return posts


def _instagram_posts():
    token = os.environ.get('INSTAGRAM_ACCESS_TOKEN', '').strip()
    if not token:
        return None

    version = os.environ.get('INSTAGRAM_GRAPH_API_VERSION', 'v25.0').strip()
    if not version.startswith('v'):
        version = f'v{version}'
    response = requests.get(
        f'https://graph.instagram.com/{version}/me/media',
        headers={'Authorization': f'Bearer {token}'},
        params={
            'fields': 'id,caption,media_type,media_product_type,permalink,media_url,thumbnail_url,timestamp',
            'limit': SOCIAL_FEED_LIMIT,
        },
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    items = response.json().get('data', [])
    posts = []
    for item in items:
        external_id = str(item.get('id') or '').strip()
        permalink = str(item.get('permalink') or '').strip()
        published_at = _utc_datetime(item.get('timestamp'))
        if not external_id or not permalink.startswith('https://www.instagram.com/') or not published_at:
            continue
        posts.append({
            'platform': 'instagram',
            'external_id': external_id,
            'caption': str(item.get('caption') or '')[:10000],
            'permalink': permalink,
            'media_type': str(item.get('media_type') or '')[:40] or None,
            'media_product_type': str(item.get('media_product_type') or '')[:40] or None,
            'media_url': item.get('media_url'),
            'thumbnail_url': item.get('thumbnail_url'),
            'published_at': published_at,
        })
    return posts


def _save_posts(platform, posts):
    synced_at = datetime.utcnow()
    for item in posts:
        post = SocialPost.query.filter_by(
            platform=platform,
            external_id=item['external_id'],
        ).first()
        if post is None:
            post = SocialPost(platform=platform, external_id=item['external_id'])
            db.session.add(post)
        for field in (
            'caption', 'permalink', 'media_type', 'media_product_type',
            'media_url', 'thumbnail_url', 'published_at',
        ):
            setattr(post, field, item[field])
        post.synced_at = synced_at
        post.is_visible = True
    db.session.commit()


def sync_social_posts():
    """Refresh configured providers while keeping cached posts on API errors."""
    providers = (
        ('linkedin', _linkedin_posts),
        ('instagram', _instagram_posts),
    )
    configured = 0
    saved = {}
    failures = []
    for platform, fetch in providers:
        try:
            posts = fetch()
            if posts is None:
                logger.info('%s social feed is not configured; skipping.', platform)
                continue
            configured += 1
            _save_posts(platform, posts)
            saved[platform] = len(posts)
            logger.info('Synced %s public %s items.', len(posts), platform)
        except (requests.RequestException, ValueError, KeyError) as error:
            db.session.rollback()
            failures.append(platform)
            logger.error('%s feed sync failed (%s).', platform, type(error).__name__)
        except Exception:
            db.session.rollback()
            failures.append(platform)
            logger.exception('%s feed sync failed unexpectedly.', platform)
    return {'configured': configured, 'saved': saved, 'failures': failures}
