import logging

logger = logging.getLogger(__name__)

class LinkedInBlogFetcher:
    """
    Safe placeholder for the optional LinkedIn feed.

    The previous implementation returned invented sample posts and engagement
    figures. Reading a member's posts requires an authorized LinkedIn API
    integration; do not substitute mock content for a real feed.
    """
    
    def __init__(self, linkedin_profile_url=None):
        self.profile_url = linkedin_profile_url or "https://www.linkedin.com/in/mayur-prabhune"
    
    def fetch_recent_posts(self, limit=3):
        logger.warning("LinkedIn feed is not configured with an approved member-posts API integration")
        return []
    
    def fetch_linkedin_articles(self, limit=3):
        logger.warning("LinkedIn article feed is not configured with an authorized API integration")
        return []
    
    def get_combined_content(self, limit=3):
        """
        Get combined posts and articles from LinkedIn
        """
        posts = self.fetch_recent_posts(limit=2)
        articles = self.fetch_linkedin_articles(limit=1)
        
        # Combine and sort by date
        all_content = posts + articles
        all_content.sort(key=lambda x: x['published_date'], reverse=True)
        
        return all_content[:limit]

def format_linkedin_content_for_blog(linkedin_content):
    """
    Format LinkedIn content to match blog post structure
    """
    formatted_posts = []
    
    for content in linkedin_content:
        formatted_post = {
            'title': content['title'],
            'excerpt': content['excerpt'],
            'url': content['url'],
            'published_at': content['published_date'],  # Changed to match template
            'created_at': content['published_date'],    # Added for consistency
            'author': content['author'],
            'source': 'LinkedIn',
            'engagement': content.get('engagement', {}),
            'tags': content.get('tags', []),
            'read_time': content.get('read_time', '5 min read'),
            'is_external': True,  # Flag to indicate this is from external source
            'image_url': None  # Added to match template expectations
        }
        formatted_posts.append(formatted_post)
    
    return formatted_posts

# Helper function to integrate with the main blog route
def get_linkedin_blog_content(limit=3):
    """
    Main function to get LinkedIn content for blog display
    """
    try:
        logger.info("Starting LinkedIn blog content fetch")
        fetcher = LinkedInBlogFetcher()
        linkedin_content = fetcher.get_combined_content(limit)
        logger.info(f"Got {len(linkedin_content)} raw LinkedIn content items")
        formatted_content = format_linkedin_content_for_blog(linkedin_content)
        logger.info(f"Formatted {len(formatted_content)} LinkedIn posts for blog")
        return formatted_content
    except Exception as e:
        logger.error(f"Error getting LinkedIn blog content: {str(e)}", exc_info=True)
        return []
