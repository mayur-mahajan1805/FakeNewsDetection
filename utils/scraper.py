import requests
from bs4 import BeautifulSoup
import re

class NewsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        })

    def scrape_url(self, url):
        """
        Scrapes the content of a news article from a given URL.
        Returns a dictionary with title and body text.
        """
        try:
            response = self.session.get(url, timeout=15)
            # Handle strict blocking
            if response.status_code in [401, 403]:
                return {
                    "success": False, 
                    "error": f"🔒 Access Denied by Site ({response.status_code}). This site has strict anti-bot protection. Please COPY & PASTE the text manually."
                }
            
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Attempt to find the main article title
            title = ""
            if soup.find('h1'):
                title = soup.find('h1').get_text(strip=True)
            else:
                title = soup.title.get_text(strip=True) if soup.title else "Unknown Title"

            # ENHANCED: Multiple strategies to find article content
            article_text = ""
            
            # Strategy 1: Look for common article containers
            article_containers = soup.find_all(['article', 'main', 'div'], class_=re.compile(r'(article|story|content|post|body)', re.I))
            if article_containers:
                for container in article_containers:
                    paragraphs = container.find_all('p')
                    valid_paragraphs = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30]
                    if valid_paragraphs:
                        article_text = " ".join(valid_paragraphs)
                        break
            
            # Strategy 2: Fallback to all paragraphs (reduced filter to 30 chars)
            if not article_text:
                paragraphs = soup.find_all('p')
                valid_paragraphs = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30]
                article_text = " ".join(valid_paragraphs)
            
            # Strategy 3: Last resort - get ALL text from body
            if len(article_text) < 100:
                body = soup.find('body')
                if body:
                    # Remove script and style elements
                    for script in body(["script", "style", "nav", "header", "footer"]):
                        script.decompose()
                    article_text = body.get_text(separator=' ', strip=True)
            
            # Cleanup
            article_text = re.sub(r'\s+', ' ', article_text).strip()
            
            # Final validation
            if len(article_text) < 100:
                return {
                    "success": False,
                    "error": "⚠️ Could not extract enough text. This site may use JavaScript to load content. Please COPY & PASTE the article text instead."
                }
            
            return {
                "success": True,
                "title": title,
                "text": article_text,
                "url": url
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
