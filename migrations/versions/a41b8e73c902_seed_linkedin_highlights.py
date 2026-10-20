"""Add curated LinkedIn highlights to the homepage feed.

Revision ID: a41b8e73c902
Revises: 3ef7c4a8219d
Create Date: 2026-10-20
"""
from datetime import datetime
from hashlib import sha256

from alembic import op
import sqlalchemy as sa


revision = 'a41b8e73c902'
down_revision = '3ef7c4a8219d'
branch_labels = None
depends_on = None


HIGHLIGHTS = [
    {
        'url': 'https://www.linkedin.com/posts/mayur-prabhune_the-biggest-mistake-i-see-in-premium-retail-activity-7488473668080254977-n3hH',
        'caption': 'Premium retail wins with relevance\n\nMayur’s L.I.S.T.E.N. approach helps advisors move beyond feature lists: understand the customer’s context, simplify the decision, tailor the recommendation, and build trust.',
    },
    {
        'url': 'https://www.linkedin.com/posts/mayur-prabhune_premiumretail-luxuryretail-retailleadership-activity-7493546920636956673-v8V5',
        'caption': 'Personalization is the starting point. Relevance builds trust.\n\nA practical perspective on using AI and customer context to make premium product recommendations feel useful to the person—not just personalized to their history.',
    },
    {
        'url': 'https://www.linkedin.com/posts/mayur-prabhune_salesenablement-aisales-salestraining-activity-7503387459041484801-nAzX',
        'caption': 'Practice the difficult sales conversation before the real call.\n\nUse AI as a rehearsal partner: give it the customer context, ask it to challenge your assumptions, then review where the conversation can improve.',
    },
]


def upgrade():
    social_post = sa.table(
        'social_post',
        sa.column('platform', sa.String),
        sa.column('external_id', sa.String),
        sa.column('caption', sa.Text),
        sa.column('permalink', sa.String),
        sa.column('media_type', sa.String),
        sa.column('media_product_type', sa.String),
        sa.column('media_url', sa.String),
        sa.column('thumbnail_url', sa.String),
        sa.column('published_at', sa.DateTime),
        sa.column('synced_at', sa.DateTime),
        sa.column('is_visible', sa.Boolean),
    )
    now = datetime.utcnow()
    op.bulk_insert(social_post, [
        {
            'platform': 'linkedin',
            'external_id': 'manual:' + sha256(item['url'].encode('utf-8')).hexdigest(),
            'caption': item['caption'],
            'permalink': item['url'],
            'media_type': None,
            'media_product_type': None,
            'media_url': None,
            'thumbnail_url': None,
            'published_at': now,
            'synced_at': now,
            'is_visible': True,
        }
        for item in HIGHLIGHTS
    ])


def downgrade():
    urls = [item['url'] for item in HIGHLIGHTS]
    op.execute(
        sa.text("DELETE FROM social_post WHERE platform = 'linkedin' AND permalink IN :urls")
        .bindparams(sa.bindparam('urls', expanding=True))
        .bindparams(urls=urls)
    )
