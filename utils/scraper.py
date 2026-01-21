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

            # Attempt to find the main article content
            # Heuristic: looking for typical article body tags
            article_text = ""
            paragraphs = soup.find_all('p')
            
            # Simple heuristic: Filter out very short paragraphs (nav links, disclaimers)
            valid_paragraphs = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50]
            article_text = " ".join(valid_paragraphs)
            
            # Cleanup
            article_text = re.sub(r'\s+', ' ', article_text).strip()
            
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
