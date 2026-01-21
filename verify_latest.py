
import os
from dotenv import load_dotenv
from advanced_engine import AdvancedTruthLens

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
news_key = os.getenv("NEWS_API_KEY")

print(f"Checking keys... Gemini: {'Yes' if gemini_key else 'No'}, News: {'Yes' if news_key else 'No'}")

engine = AdvancedTruthLens(gemini_key, news_key)

print("--- Testing Trending News (Latest News) ---")
try:
    articles = engine.get_trending_news()
    if articles:
        print(f"SUCCESS: Fetched {len(articles)} articles.")
        print(f"Sample: {articles[0]['title']} ({articles[0]['publishedAt']})")
    else:
        print("FAILURE: No articles returned (but no crash).")
except Exception as e:
    print(f"ERROR: News fetch failed: {e}")

print("\n--- Testing Gemini Model (Latest Model) ---")
try:
    # prompt it with something simple
    res = engine.analyze_article_with_gemini("This is a test article to check the model.")
    if "error" in res:
        print(f"FAILURE: Model returned error: {res['message']}")
    else:
        print("SUCCESS: Model analyzed text.")
except Exception as e:
    print(f"ERROR: Model call crashed: {e}")
