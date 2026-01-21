import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Poppins:wght@700;800;900&family=Space+Grotesk:wght@700&display=swap');

        /* General App Styling - Deep Navy Background for "Truth" Theme */
        .stApp {
            background: radial-gradient(circle at top left, #1e3a8a 0%, #0f172a 50%, #020617 100%);
            font-family: 'Inter', sans-serif;
            color: #e2e8f0;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.8);
            backdrop-filter: blur(12px);
            border-right: 1px solid rgba(59, 130, 246, 0.2);
        }

        /* Custom Card/Container Style - Blue Tint Glass */
        .glass-card {
            background: rgba(30, 58, 138, 0.15); /* Tinted with Deep Blue */
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(56, 189, 248, 0.15); /* Light Cyan Border */
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s;
        }
        
        .glass-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(14, 165, 233, 0.15), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(56, 189, 248, 0.4); /* Brighter Cyan on Hover */
        }

        /* Metrics Styling */
        div[data-testid="stMetricValue"] {
            font-size: 28px;
            font-weight: 800;
            color: #38bdf8; /* Sky Blue */
            text-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        }
        
        div[data-testid="stMetricLabel"] {
            color: #94a3b8;
            font-size: 14px;
            font-weight: 600;
        }

        /* Input Areas */
        .stTextArea textarea, .stTextInput input {
            background-color: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(59, 130, 246, 0.3) !important;
            color: #f8fafc !important;
            border-radius: 12px !important;
        }
        
        .stTextArea textarea:focus, .stTextInput input:focus {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.3) !important;
        }

        /* Buttons - Trust Blue Gradient */
        .stButton button {
            background: linear-gradient(135deg, #2563eb 0%, #0284c7 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 12px;
            font-weight: 700;
            transition: all 0.3s ease;
            box-shadow: 0 4px 14px 0 rgba(2, 132, 199, 0.3);
        }
        
        .stButton button:hover {
            background: linear-gradient(135deg, #1d4ed8 0%, #0369a1 100%);
            box-shadow: 0 6px 20px rgba(2, 132, 199, 0.5);
            transform: scale(1.02);
        }

        /* Headers */
        h1, h2, h3 {
            color: white;
            font-weight: 800;
            letter-spacing: -0.025em;
        }
        
        h1 {
            background: linear-gradient(to right, #60a5fa, #38bdf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem !important;
        }

        /* Highlight Tags - Updated Colors */
        .highlight-tag {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            margin-right: 8px;
            margin-bottom: 8px;
        }
        
        .tag-red { background: rgba(220, 38, 38, 0.2); color: #fca5a5; border: 1px solid rgba(220, 38, 38, 0.4); } /* Deeper error red */
        .tag-green { background: rgba(16, 185, 129, 0.2); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.4); } /* Emerald green */
        .tag-yellow { background: rgba(234, 179, 8, 0.2); color: #fde047; border: 1px solid rgba(234, 179, 8, 0.4); }
        .tag-blue { background: rgba(59, 130, 246, 0.3); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.5); }

        /* Animations */
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; box-shadow: 0 0 10px rgba(56, 189, 248, 0.2); }
            50% { opacity: 0.8; box-shadow: 0 0 20px rgba(56, 189, 248, 0.5); }
        }

        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }

        /* Apply animations */
        .stApp > div:first-child { animation: fadeIn 0.8s ease-out; }
        div[data-testid="stHorizontalBlock"] { animation: fadeInDown 0.6s ease-out; }
        .glass-card { animation: fadeIn 0.8s ease-out; }

        /* Badge pulse animation - Blue Theme */
        span[style*="background: rgba(14, 165, 233"] { animation: pulse 2.5s ease-in-out infinite; } /* Cyan/Blue Badge */

        /* Smooth scroll */
        html { scroll-behavior: smooth; }

        /* Loading animation for progress bars */
        .stProgress > div > div {
            background: linear-gradient(90deg, #0ea5e9 0%, #3b82f6 50%, #0ea5e9 100%);
            background-size: 200% 100%;
            animation: shimmer 2s linear infinite;
        }

        /* Expander animation */
        .streamlit-expanderHeader { transition: all 0.3s ease; background-color: rgba(30, 58, 138, 0.3) !important; border-radius: 10px; }
        .streamlit-expanderHeader:hover { background-color: rgba(30, 58, 138, 0.5) !important; transform: translateX(5px); }
        </style>
    """, unsafe_allow_html=True)
