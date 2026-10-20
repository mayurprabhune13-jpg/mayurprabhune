"""One-shot Railway Cron entry point for the social feed cache."""
import logging
import sys

from app import create_app, db
from app.social_sync import sync_social_posts
from config_prod import ProductionConfig


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')


def main():
    app = create_app(ProductionConfig)
    with app.app_context():
        result = sync_social_posts()
        db.session.remove()
        db.engine.dispose()
    if not result['configured']:
        logging.getLogger(__name__).info('No social API credentials configured; sync skipped.')
        return 0
    if result['failures']:
        logging.getLogger(__name__).error('Some social feeds failed: %s', ', '.join(result['failures']))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
