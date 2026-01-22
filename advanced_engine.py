import google.generativeai as genai
import json
import os
import joblib
import re
import string
from newsapi import NewsApiClient

def clean_text(text):
    if not isinstance(text, str): return ""
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(f'[{re.escape(string.punctuation)}]', '', text)
    text = re.sub(r'\n', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

class AdvancedTruthLens:
    def __init__(self, gemini_key=None, news_api_key=None):
        self.gemini_key = gemini_key
        self.news_api_key = news_api_key
        
        # Load local ML model if exists
        self.local_model = None
        self.vectorizer = None
        try:
            if os.path.exists("models/truthlens_model.pkl"):
                self.local_model = joblib.load("models/truthlens_model.pkl")
                self.vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
                print("✅ Local ML Model Loaded")
        except Exception as e:
            print(f"⚠️ Could not load local model: {e}")
        
        if self.gemini_key:
            genai.configure(api_key=self.gemini_key)
            # Switching to 'gemini-flash-latest' (High-limit production model found in your list)
            self.model = genai.GenerativeModel('gemini-flash-latest')
            
        if self.news_api_key:
            self.newsapi = NewsApiClient(api_key=self.news_api_key)

    def analyze_article_with_gemini(self, text):
        """
        Uses Gemini to perform deep fake news analysis.
        Returns a structured JSON response.
        """
        
        # 1. Local Model Prediction (Fast Check)
        local_score = "N/A"
        local_pred = "Uncertain"
        
        if self.local_model:
            try:
                # Essential: Apply same cleaning as training!
                cleaned_input = clean_text(text)
                vec = self.vectorizer.transform([cleaned_input])
                pred = self.local_model.predict(vec)[0]
                
                local_pred = pred
                local_score = 90 if pred == "REAL" else 10
            except:
                pass

        if not self.gemini_key:
            return {"error": "Authentication Missing", "message": "Please provide a Gemini API Key."}

        # Chain-of-Thought Prompting for Higher Accuracy
        prompt = f"""
        Act as an expert Disinformation Analyst. Your task is to provide a final credibility verification for the text below.
        
        CONTEXT: 
        1. An internal ML Model (PassiveAggressive Classifier) analyzed this text.
        2. Local Model Verdict: {local_pred}
        3. Local Model Confidence: {local_score}%
        
        INSTRUCTIONS:
        - Step 1: Analyze the Local Model's verdict. If it says FAKE, look deeply for linguistic patterns of deception (hedging, inflammatory language).
        - Step 2: Cross-examine with your own knowledge base. Are the facts consistent with established reality?
        - Step 3: Check for "Clickbait Dissonance". Does the headline match the body?
        - Step 4: Synthesize both inputs into a final score.
        
        Article Text: "{text[:4000]}..."
        
        Return a valid JSON object with ONLY this structure:
        {{
            "credibility_score": <int 0-100 representing trustworthiness>,
            "classification": "<Reliable/Questionable/Unreliable/Satire>",
            "summary": "<Concise executive summary>",
            "clickbait_analysis": {{
                "is_clickbait": <bool>,
                "dissonance_score": <int 0-100>,
                "reason": "<Why it is/is not clickbait>"
            }},
            "bias_analysis": {{
                "political_spectrum": "<Left/Center-Left/Center/Center-Right/Right>",
                "emotional_tone": "<Neutral/Angry/Fear/Joy>"
            }},
            "fallacies": ["<List 2-3 specific logical fallacies if found>"],
            "key_entities": [
                {{"name": "<Name>", "sentiment_score": <float -1.0 to 1.0>, "type": "<Person/Org>"}}
            ],
            "sensationalism_rating": <int 0-100>,
            "fact_check_recommendation": "<True/False>"
        }}
        """
        
        
        try:
            response = self.model.generate_content(prompt)
            
            # Check if response was blocked by safety filters
            if not response.parts:
                return {
                    "error": "Content Blocked", 
                    "message": "⚠️ Gemini's safety filters flagged this content as potentially harmful or violating content policies. This often happens with extreme conspiracy theories or medical misinformation. Try analyzing a different article or use more neutral language."
                }
            
            # Cleanup json (sometimes model returns ```json ... ```)
            raw_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(raw_text)
        except AttributeError as e:
            # Happens when response.text fails due to safety block
            return {
                "error": "Safety Block", 
                "message": "🛡️ This content was blocked by Gemini's safety filters. The text may contain extreme misinformation, hate speech, or policy violations. Please try a different article."
            }
        except json.JSONDecodeError as e:
            return {
                "error": "Invalid Response", 
                "message": f"⚠️ Gemini returned invalid data. This sometimes happens with very short or unusual text. Error: {str(e)}"
            }
        except Exception as e:
            return {"error": "Analysis Failed", "message": str(e)}

    def get_trending_news(self, topic="general"):
        """
        Fetches trending news using NewsAPI
        """
        if not self.news_api_key:
            return []

        try:
            # Fetch top headlines
            top_headlines = self.newsapi.get_top_headlines(
                language='en',
                country='us',
                page_size=10
            )
            
            articles = []
            for art in top_headlines.get('articles', []):
                articles.append({
                    "title": art['title'],
                    "source": art['source']['name'],
                    "url": art['url'],
                    "image": art['urlToImage'],
                    "publishedAt": art['publishedAt'],
                    "description": art['description']
                })
            return articles
            
        except Exception as e:
            print(f"News API Error: {e}")
            return []
