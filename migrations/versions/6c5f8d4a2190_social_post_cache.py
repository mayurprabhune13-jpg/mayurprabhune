"""Create a cache for authorized LinkedIn and Instagram feed items.

Revision ID: 6c5f8d4a2190
Revises: bb2dbb6b4eaa
Create Date: 2026-10-20
"""
from alembic import op
import sqlalchemy as sa


revision = '6c5f8d4a2190'
down_revision = 'bb2dbb6b4eaa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'social_post',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('platform', sa.String(length=20), nullable=False),
        sa.Column('external_id', sa.String(length=255), nullable=False),
        sa.Column('caption', sa.Text(), nullable=True),
        sa.Column('permalink', sa.String(length=1000), nullable=False),
        sa.Column('media_type', sa.String(length=40), nullable=True),
        sa.Column('media_product_type', sa.String(length=40), nullable=True),
        sa.Column('media_url', sa.String(length=2048), nullable=True),
        sa.Column('thumbnail_url', sa.String(length=2048), nullable=True),
        sa.Column('published_at', sa.DateTime(), nullable=False),
        sa.Column('synced_at', sa.DateTime(), nullable=False),
        sa.Column('is_visible', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('platform', 'external_id', name='uq_social_post_platform_external_id'),
    )
    op.create_index('ix_social_post_published_at', 'social_post', ['published_at'])
    op.create_index('ix_social_post_platform_published_at', 'social_post', ['platform', 'published_at'])


def downgrade():
    op.drop_index('ix_social_post_platform_published_at', table_name='social_post')
    op.drop_index('ix_social_post_published_at', table_name='social_post')
    op.drop_table('social_post')
