import requests
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class LinkedInBlogFetcher:
    """
    Fetches blog posts from LinkedIn using various methods
    """
    
    def __init__(self, linkedin_profile_url=None):
        self.profile_url = linkedin_profile_url or "https://www.linkedin.com/in/mayur-prabhune"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_recent_posts(self, limit=3):
        """
        Fetch recent LinkedIn posts/articles
        Since LinkedIn's API is restricted, this returns mock data for now
        In production, you would integrate with LinkedIn's API or use authorized RSS feeds
        """
        try:
            # For now, return sample blog posts that would be typical for an AI mentor
            sample_posts = [
                {
                    'title': 'The Future of AI Leadership: 5 Key Trends Every Executive Should Know',
                    'excerpt': 'As AI continues to reshape industries, leaders must adapt their strategies. Here are the critical trends that will define AI leadership in 2024 and beyond.',
                    'url': f"{self.profile_url}/recent-activity/",
                    'published_date': datetime.now() - timedelta(days=2),
                    'author': 'Mayur Prabhune',
                    'engagement': {'likes': 156, 'comments': 23, 'shares': 12},
                    'tags': ['AI Leadership', 'Executive Strategy', 'Digital Transformation']
                },
                {
                    'title': 'Ethical AI Implementation: A Practical Framework for Indian Businesses',
                    'excerpt': 'Implementing AI ethically requires more than good intentions. This framework helps Indian businesses navigate cultural considerations while adopting AI responsibly.',
                    'url': f"{self.profile_url}/recent-activity/",
                    'published_date': datetime.now() - timedelta(days=5),
                    'author': 'Mayur Prabhune',
                    'engagement': {'likes': 234, 'comments': 34, 'shares': 18},
                    'tags': ['Ethical AI', 'Cultural Sensitivity', 'Business Strategy']
                },
                {
                    'title': 'Breaking Down AI Silos: How Cross-Functional Teams Drive Innovation',
                    'excerpt': 'AI success isn\'t just about technology—it\'s about people. Learn how building cross-functional AI teams can accelerate innovation and ensure sustainable adoption.',
                    'url': f"{self.profile_url}/recent-activity/",
                    'published_date': datetime.now() - timedelta(days=8),
                    'author': 'Mayur Prabhune',
                    'engagement': {'likes': 187, 'comments': 28, 'shares': 15},
                    'tags': ['Team Building', 'AI Innovation', 'Organizational Change']
                }
            ]
            
            return sample_posts[:limit]
            
        except Exception as e:
            logger.error(f"Error fetching LinkedIn posts: {str(e)}")
            return []
    
    def fetch_linkedin_articles(self, limit=3):
        """
        Fetch published LinkedIn articles
        This would integrate with LinkedIn's Publishing API in production
        """
        try:
            # Sample LinkedIn articles for AI mentor
            sample_articles = [
                {
                    'title': 'The ETHICS Framework: A Comprehensive Guide to Responsible AI Implementation',
                    'excerpt': 'Introducing the ETHICS framework - a systematic approach to implementing AI that prioritizes cultural sensitivity, transparency, and sustainable business outcomes.',
                    'url': f"{self.profile_url}/pulse/",
                    'published_date': datetime.now() - timedelta(days=12),
                    'author': 'Mayur Prabhune',
                    'read_time': '8 min read',
                    'engagement': {'likes': 312, 'comments': 45, 'shares': 28},
                    'tags': ['ETHICS Framework', 'AI Implementation', 'Responsible AI']
                },
                {
                    'title': 'Leading AI Transformation: Lessons from 50+ Indian Organizations',
                    'excerpt': 'After working with over 50 Indian organizations on AI transformation, here are the key patterns that separate successful AI leaders from the rest.',
                    'url': f"{self.profile_url}/pulse/",
                    'published_date': datetime.now() - timedelta(days=20),
                    'author': 'Mayur Prabhune',
                    'read_time': '12 min read',
                    'engagement': {'likes': 489, 'comments': 67, 'shares': 41},
                    'tags': ['AI Transformation', 'Leadership', 'Case Studies']
                }
            ]
            
            return sample_articles[:limit]
            
        except Exception as e:
            logger.error(f"Error fetching LinkedIn articles: {str(e)}")
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
            'published_date': content['published_date'],
            'author': content['author'],
            'source': 'LinkedIn',
            'engagement': content.get('engagement', {}),
            'tags': content.get('tags', []),
            'read_time': content.get('read_time', '5 min read'),
            'is_external': True  # Flag to indicate this is from external source
        }
        formatted_posts.append(formatted_post)
    
    return formatted_posts

# Helper function to integrate with the main blog route
def get_linkedin_blog_content(limit=3):
    """
    Main function to get LinkedIn content for blog display
    """
    try:
        fetcher = LinkedInBlogFetcher()
        linkedin_content = fetcher.get_combined_content(limit)
        return format_linkedin_content_for_blog(linkedin_content)
    except Exception as e:
        logger.error(f"Error getting LinkedIn blog content: {str(e)}")
        return []