"""Add editable site identity, SEO and homepage settings."""
from alembic import op
import sqlalchemy as sa


revision = '3ef7c4a8219d'
down_revision = '6c5f8d4a2190'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'site_settings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('site_name', sa.String(length=120), nullable=False, server_default='Mayur Prabhune'),
        sa.Column('brand_tagline', sa.String(length=180), nullable=False, server_default='AI · LEARNING · ENABLEMENT'),
        sa.Column('seo_title', sa.String(length=180), nullable=False, server_default='AI, Learning & Sales Enablement'),
        sa.Column('seo_description', sa.String(length=320), nullable=False, server_default='Practical AI learning, workforce capability, and sales enablement with Mayur Prabhune.'),
        sa.Column('homepage_eyebrow', sa.String(length=180), nullable=False, server_default='AI / Learning / Enablement'),
        sa.Column('homepage_headline', sa.String(length=220), nullable=False, server_default='Building Human Potential in the Age of AI.'),
        sa.Column('homepage_support', sa.String(length=240), nullable=False, server_default='Generative AI · Learning Innovation · Retail & Sales Enablement'),
        sa.Column('homepage_intro', sa.Text(), nullable=False, server_default='I help people and teams connect new technology and learning with the work they do every day—from exploring AI to strengthening customer conversations.'),
        sa.Column('homepage_photo_url', sa.String(length=500), nullable=True),
        sa.Column('featured_video_title', sa.String(length=200), nullable=False, server_default='Featured talk on AI leadership'),
        sa.Column('featured_video_description', sa.String(length=500), nullable=False, server_default='Get a glimpse into the world of AI leadership with this featured talk.'),
        sa.Column('featured_video_url', sa.String(length=500), nullable=False, server_default='https://www.youtube.com/watch?v=f_Px9x503N0'),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('site_settings')
