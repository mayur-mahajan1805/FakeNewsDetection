import json
import os
import streamlit as st
import datetime

STATS_FILE = "data/history.json"

class StatsManager:
    def __init__(self):
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(STATS_FILE):
             with open(STATS_FILE, "w") as f:
                 json.dump([], f)
    
    def log_analysis(self, result, article_text=""):
        """
        Saves a complete record of the analysis including article text.
        """
        record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "verdict": result.get('classification', 'Unknown'),
            "score": result.get('credibility_score', 0),
            "is_clickbait": result.get('clickbait_analysis', {}).get('is_clickbait', False),
            "bias": result.get('bias_analysis', {}).get('political_spectrum', 'Neutral'),
            "summary": result.get('summary', 'No summary available'),
            "article_snippet": article_text[:300] + "..." if len(article_text) > 300 else article_text,
            "article_full": article_text,  # Store full text for PDF regeneration
            "full_analysis": result  # Store complete analysis for report generation
        }
        
        try:
            with open(STATS_FILE, "r") as f:
                history = json.load(f)
            history.append(record)
            with open(STATS_FILE, "w") as f:
                json.dump(history, f, indent=2)
        except:
            pass # Fail silently in demo to avoid blocking UI

    def get_stats(self):
        try:
            with open(STATS_FILE, "r") as f:
                data = json.load(f)
            
            if not data:
                return None
                
            total = len(data)
            fake_count = sum(1 for x in data if "Unreliable" in x['verdict'] or "Questionable" in x['verdict'])
            real_count = sum(1 for x in data if "Reliable" in x['verdict'])
            satire_count = sum(1 for x in data if "Satire" in x['verdict'])
            
            avg_score = sum(x['score'] for x in data) / total if total > 0 else 0
            
            return {
                "total": total,
                "fake": fake_count,
                "real": real_count,
                "satire": satire_count,
                "avg_score": int(avg_score),
                "history": data # Return full list for charts
            }
        except:
            return None
