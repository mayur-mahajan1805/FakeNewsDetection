"""
Gemini API Quota Checker
This script checks your current Gemini API usage and limits.
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_api_quota():
    """
    Check Gemini API quota and usage.
    Note: Google's Gemini API doesn't provide direct quota checking via API.
    This script will make a test request and show rate limit information.
    """
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env file")
        return
    
    print("🔍 Checking Gemini API Status...\n")
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-4:]}")
    print("-" * 50)
    
    try:
        # Configure API
        genai.configure(api_key=api_key)
        
        # List available models
        print("\n✅ API Key is Valid!")
        print("\n📋 Available Models:")
        
        model_count = 0
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                model_count += 1
                print(f"  {model_count}. {model.name}")
                if model_count >= 5:  # Show first 5 models
                    break
        
        # Make a test request to check if API is working
        print("\n🧪 Testing API with a simple request...")
        test_model = genai.GenerativeModel('gemini-flash-latest')
        response = test_model.generate_content("Say 'API is working'")
        
        print("✅ Test Request Successful!")
        print(f"📝 Response: {response.text}")
        
        # Display quota information
        print("\n" + "=" * 50)
        print("📊 QUOTA INFORMATION")
        print("=" * 50)
        
        print("\n🆓 Free Tier Limits (Gemini API):")
        print("  • Requests per minute (RPM): 15")
        print("  • Requests per day (RPD): 1,500")
        print("  • Tokens per minute (TPM): 1,000,000")
        
        print("\n💡 How to Check Your Actual Usage:")
        print("  1. Visit: https://aistudio.google.com/app/apikey")
        print("  2. Click on your API key")
        print("  3. View usage statistics and quotas")
        
        print("\n⚠️ Note: Google doesn't provide programmatic quota checking.")
        print("   You must check the AI Studio dashboard for exact numbers.")
        
        print("\n" + "=" * 50)
        print("✅ API Check Complete!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n💡 Common Issues:")
        print("  • Invalid API key")
        print("  • Quota exceeded")
        print("  • Network connection issues")
        print("  • API key not enabled for Gemini")

if __name__ == "__main__":
    check_api_quota()
