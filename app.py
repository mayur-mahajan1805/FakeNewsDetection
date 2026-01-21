import streamlit as st
import base64
import plotly.graph_objects as go
import time
from utils.scraper import NewsScraper
from utils.report_generator import generate_pdf_report
from utils.styles import apply_custom_styles
from utils.stats_manager import StatsManager
from advanced_engine import AdvancedTruthLens
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Config & Setup ---
st.set_page_config(
    page_title="TruthLens AI - Detect Fake News with AI Precision",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_custom_styles()
stats_manager = StatsManager()

# --- Helpers ---
def go_to_analysis(url):
    st.session_state.active_tab = "Analyzer"
    st.session_state.url_to_analyze = url

# Initialize session state
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Home"

# --- Helpers for Visuals ---

def draw_gauge_chart(score):
    color = "red"
    if score > 40: color = "orange"
    if score > 70: color = "#34d399" 
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Credibility Confidence", 'font': {'size': 24, 'color': "white"}},
        number = {'font': {'size': 50, 'color': "white"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255, 0.3)",
            'steps': [
                {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.3)'},
                {'range': [40, 70], 'color': 'rgba(251, 191, 36, 0.3)'},
                {'range': [70, 100], 'color': 'rgba(52, 211, 153, 0.3)'}],
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white", 'family': "Inter"}, height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

def draw_radar_chart(data):
    features = ['Subjectivity', 'Sensationalism', 'Bias Risk', 'Logical Consistency', 'Factuality']
    # Mapping Gemini data to these 5 axes
    
    # Heuristics to map the JSON response to radar chart
    subj = data['bias_analysis'].get('subjectivity_score', 50)
    sens = data.get('sensationalism_rating', 50)
    bias = 100 if data['bias_analysis'].get('political_spectrum') != 'Center' else 20
    logic = 100 - (len(data.get('fallacies', [])) * 20) # Penalize fallacies
    fact = data.get('credibility_score', 50)
    
    values = [subj, sens, bias, max(0, logic), fact]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=features,
        fill='toself',
        name='Article Metrics',
        line_color='#38bdf8',
        fillcolor='rgba(56, 189, 248, 0.2)'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(color='gray'), gridcolor='rgba(255,255,255,0.1)'),
            angularaxis=dict(tickfont=dict(color='white', size=14), linecolor='rgba(255,255,255,0.1)'),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=350,
        margin=dict(l=40, r=40, t=20, b=20)
    )
    return fig

def draw_entity_chart(entities):
    if not entities:
        return go.Figure()
        
    names = [e['name'] for e in entities]
    # Map score -1..1 to color intensity or category
    colors = []
    for e in entities:
        score = e['sentiment_score']
        if score > 0.3: colors.append('#34d399') # Green
        elif score < -0.3: colors.append('#ef4444') # Red
        else: colors.append('#94a3b8') # Grey
        
    fig = go.Figure(data=[go.Pie(
        labels=names,
        values=[abs(e['sentiment_score']) + 0.5 for e in entities], # Size adjustment
        hole=.4,
        marker_colors=colors,
        textinfo='label',
        hoverinfo='label+percent'
    )])
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Inter"},
        height=300,
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False
    )
    return fig

# --- Load API Keys (Hidden, from environment) ---
gemini_key = os.getenv("GEMINI_API_KEY")
news_key = os.getenv("NEWS_API_KEY")

# --- Top Navigation Bar ---
# --- Load and Encode Logo ---
def get_logo_base64():
    with open("logo_final.svg", "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

logo_base64 = get_logo_base64()

# --- Top Navigation Bar ---
st.markdown(f"""
<div style="background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); padding: 1rem 2rem; border-radius: 15px; margin-bottom: 2rem; box-shadow: 0 8px 32px rgba(2, 6, 23, 0.5); border: 1px solid rgba(59, 130, 246, 0.2);">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 1.5rem;">
            <img src="data:image/svg+xml;base64,{logo_base64}" alt="TruthLens Logo" width="60" height="60" style="filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.3));">
            <h1 style="
                margin: 0; 
                font-size: 2.2rem; 
                font-family: 'Poppins', sans-serif; 
                font-weight: 800; 
                background: linear-gradient(135deg, #ffffff 0%, #38bdf8 50%, #0ea5e9 100%); 
                -webkit-background-clip: text; 
                -webkit-text-fill-color: transparent;
                letter-spacing: -0.02em;
                text-shadow: 0 0 30px rgba(56, 189, 248, 0.2);
            ">TruthLens AI</h1>
        </div>
        <div style="font-size: 0.85rem; color: #cbd5e1; display: flex; align-items: center; gap: 0.5rem;">
            <span style="background: rgba(14, 165, 233, 0.2); padding: 0.4rem 1rem; border-radius: 20px; border: 1px solid rgba(14, 165, 233, 0.3); font-weight: 600;">⚡ Powered by Gemini AI</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Navigation Tabs ---
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

with col1:
    if st.button("🏠 Home", key="nav_home", use_container_width=True):
        st.session_state.active_tab = "Home"
with col2:
    if st.button("🔍 Analyzer", key="nav_analyzer", use_container_width=True):
        st.session_state.active_tab = "Analyzer"
with col3:
    if st.button("📰 Trending News", key="nav_trending", use_container_width=True):
        st.session_state.active_tab = "Trending News"
with col4:
    if st.button("📊 History", key="nav_history", use_container_width=True):
        st.session_state.active_tab = "History"
with col5:
    if st.button("📈 Stats", key="nav_stats", use_container_width=True):
        st.session_state.active_tab = "Stats"

st.markdown("<br>", unsafe_allow_html=True)

# --- HOME / DASHBOARD PAGE ---
if st.session_state.active_tab == "Home":
    # Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem; background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%); border-radius: 20px; margin-bottom: 3rem;">
        <h1 style="font-size: 3.5rem; margin-bottom: 1rem; background: linear-gradient(90deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Detect Fake News with<br><span style="color: #818cf8;">AI Precision</span>
        </h1>
        <p style="font-size: 1.2rem; color: #94a3b8; max-width: 800px; margin: 0 auto; line-height: 1.8;">
            Advanced machine learning algorithms analyze news articles in real-time, providing instant credibility assessment with explainable AI insights and trending news from multiple sources.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("### ✨ Key Features")
    
    feat1, feat2, feat3 = st.columns(3)
    
    with feat1:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
            <h3 style="color: #60a5fa;">Hybrid AI Analysis</h3>
            <p style="color: #94a3b8;">Combines local ML model (99% accuracy) with Google Gemini for deep reasoning and fact-checking.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📡</div>
            <h3 style="color: #a78bfa;">Real-Time Intelligence</h3>
            <p style="color: #94a3b8;">Live web scraping and global news feeds powered by NewsAPI for instant verification.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feat3:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📄</div>
            <h3 style="color: #34d399;">Professional Reports</h3>
            <p style="color: #94a3b8;">One-click PDF export with detailed analysis, bias detection, and logical fallacy identification.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # How It Works Section
    st.markdown("### 🔄 How It Works")
    
    step1, step2, step3, step4 = st.columns(4)
    
    with step1:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: rgba(96, 165, 250, 0.1); border-radius: 15px; border-left: 4px solid #60a5fa;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">1️⃣</div>
            <h4 style="color: #60a5fa;">Input Article</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">Paste text or URL</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step2:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: rgba(168, 85, 247, 0.1); border-radius: 15px; border-left: 4px solid #a855f7;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">2️⃣</div>
            <h4 style="color: #a855f7;">AI Analysis</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">Hybrid ML + LLM</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step3:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: rgba(34, 197, 94, 0.1); border-radius: 15px; border-left: 4px solid #22c55e;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">3️⃣</div>
            <h4 style="color: #22c55e;">Get Results</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">Instant verdict</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step4:
        st.markdown("""
        <div style="text-align: center; padding: 1.5rem; background: rgba(251, 191, 36, 0.1); border-radius: 15px; border-left: 4px solid #fbbf24;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">4️⃣</div>
            <h4 style="color: #fbbf24;">Export Report</h4>
            <p style="color: #94a3b8; font-size: 0.9rem;">Download PDF</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # CTA Section
    st.markdown("""
    <div style="text-align: center; padding: 3rem 2rem; background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.15) 100%); border-radius: 20px; margin-top: 2rem;">
        <h2 style="color: #818cf8; margin-bottom: 1rem;">Ready to Verify Your News?</h2>
        <p style="color: #94a3b8; margin-bottom: 2rem;">Start analyzing articles with AI-powered fact-checking now.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_cta1, col_cta2, col_cta3 = st.columns([1, 1, 1])
    with col_cta2:
        if st.button("🚀 Start Analyzing", key="cta_analyze", use_container_width=True, type="primary"):
            st.session_state.active_tab = "Analyzer"
            st.rerun()

# --- ANALYZER PAGE ---
elif st.session_state.active_tab == "Analyzer":
    if not gemini_key:
        st.warning("⚠️ Please add your GEMINI_API_KEY to the .env file to use analysis features.")
        st.stop()
        
    engine = AdvancedTruthLens(gemini_key, news_key)
    scraper = NewsScraper()
    
    st.markdown("### 🔍 Article Inspector")
    
    input_method = st.tabs(["📝 Paste Text", "🔗 Analyze URL"])
    
    article_content = ""
    
    with input_method[0]:
        user_text = st.text_area("Paste Article content...", height=200)
        if st.button("Analyze Text"):
            article_content = user_text

    with input_method[1]:
        # Intelligent URL Input: Prefill if coming from Feed
        default_url = st.session_state.get('url_to_analyze', "")
        
        # We bind the text input to a key so it syncs with session state automatically
        url_input = st.text_input("Enter Article URL", value=default_url, key="url_input_widget")
        
        # Sync widget back to state if user typed manually
        if url_input != default_url:
             st.session_state.url_to_analyze = url_input
            
        if st.button("Scrape & Analyze"):
            if not url_input:
                st.warning("Please enter a URL first.")
            else:
                with st.status("🕷️ Scraping Article...", expanded=True) as status:
                    result = scraper.scrape_url(url_input)
                    if result['success']:
                        status.update(label="✅ Scraped Successfully!", state="complete", expanded=False)
                        article_content = result['text']
                        st.success(f"Loaded: {result['title']}")
                        
                        # NEW: Show Extracted Text
                        with st.expander("📄 View Extracted Text", expanded=False):
                            st.markdown(f"_{article_content[:2000]}..._")
                            if len(article_content) > 2000:
                                st.caption("(Text truncated for preview)")
                    else:
                        status.update(label="❌ Scraping Failed", state="error")
                        st.error(result['error'])

    if article_content and len(article_content) > 50:
        
        # Animated Loading
        progress_text = "Analysis in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        
        with st.spinner("🤖 TruthLens AI is active..."):
            time.sleep(0.5)
            my_bar.progress(20, text="Reading semantic structure...")
            
            # Call Gemini
            analysis = engine.analyze_article_with_gemini(article_content)
            my_bar.progress(60, text="Detecting logical fallacies & bias...")
            time.sleep(0.5)
            my_bar.progress(90, text="Generating visualizing...")
            time.sleep(0.3)
            my_bar.empty()

            if "error" in analysis:
                st.error(analysis['message'])
            else:
                # Log Stats with article text
                stats_manager.log_analysis(analysis, article_content)
                
                # --- RESULTS DASHBOARD ---
                st.markdown("---")
                
                # 1. Headline Stats (Clickbait & Executive Summary)
                c_cb, c_sum = st.columns([1, 2])
                
                with c_cb:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown("### 🎣 Clickbait Detector")
                    cb_data = analysis.get('clickbait_analysis', {})
                    is_cb = cb_data.get('is_clickbait', False)
                    score = cb_data.get('dissonance_score', 0)
                    
                    color = "#ef4444" if is_cb else "#34d399"
                    status = "Likely Clickbait" if is_cb else "Trustworthy Headline"
                    
                    st.markdown(f"""
                        <div style="text-align:center;">
                            <h2 style="color:{color}; margin:0;">{score}%</h2>
                            <p style="opacity:0.8;">Dissonance Score</p>
                            <div style="background:{color}; padding:5px; border-radius:5px; margin-top:10px; font-weight:bold;">{status}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.markdown(f"**Reason:** {cb_data.get('reason', 'N/A')}")
                    st.markdown('</div>', unsafe_allow_html=True)

                with c_sum:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown("### 📋 Executive Summary") 
                    st.info(analysis.get('summary', 'No summary available.'))
                    
                    sc1, sc2 = st.columns(2)
                    with sc1:
                        st.markdown(f"**Political Leaning:** {analysis['bias_analysis']['political_spectrum']}")
                        st.markdown(f"**Tone:** {analysis['bias_analysis']['emotional_tone']}")
                    with sc2:
                        st.markdown(f"**Sensationalism:** {analysis.get('sensationalism_rating', 0)}/100")
                        st.markdown(f"**Fact-Check Needed:** {analysis.get('fact_check_recommendation', 'False')}")
                    st.markdown('</div>', unsafe_allow_html=True)

                # 2. Deep Metrics (Gauge & Radar)
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.plotly_chart(draw_gauge_chart(analysis['credibility_score']), use_container_width=True)
                    st.markdown(f"<div style='text-align:center; font-size:1.2rem; font-weight:bold; color:white;'>Verdict: {analysis['classification']}</div>", unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with c2:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown("### 🕸️ Bias Radar")
                    st.plotly_chart(draw_radar_chart(analysis), use_container_width=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # 3. Entities & Fallacies
                c3, c4 = st.columns([1, 1])
                
                with c3:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown("### 👥 Entity Sentiment")
                    entities = analysis.get('key_entities', [])
                    if entities:
                        st.plotly_chart(draw_entity_chart(entities), use_container_width=True)
                    else:
                        st.markdown("No major entities detected.")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                with c4:
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.markdown("### ⚠️ Logical Fallacies Detected")
                    if analysis.get('fallacies'):
                        for f in analysis['fallacies']:
                             st.markdown(f'<div style="padding:10px; background:rgba(239, 68, 68, 0.2); border-left:4px solid #ef4444; margin-bottom:10px; border-radius:4px;">{f}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown("✅ No major logical fallacies detected.")
                    st.markdown('</div>', unsafe_allow_html=True)

                # 4. Export Report
                st.markdown("### 📄 Export Analysis")
                pdf_bytes = generate_pdf_report(article_content, analysis)
                st.download_button(
                    label="Download Full Report (PDF)",
                    data=pdf_bytes,
                    file_name="truthlens_report.pdf",
                    mime="application/pdf",
                    key="download-pdf"
                )
                    
# --- TRENDING NEWS PAGE ---
elif st.session_state.active_tab == "Trending News":
    st.markdown("### 📰 Live Global Headliners")
    
    if not news_key:
        st.warning("⚠️ Please add NEWS_API_KEY to your .env file to see trending stories.")
    else:
        engine = AdvancedTruthLens(gemini_key, news_key)
        articles = engine.get_trending_news()
        
        # Grid layout for news
        for i in range(0, len(articles), 2):
            c1, c2 = st.columns(2)
            
            # Article 1
            with c1:
                a = articles[i]
                with st.container():
                    st.markdown(f"""
                    <div class="glass-card">
                        <img src="{a['image']}" style="width:100%; border-radius:10px; height:180px; object-fit:cover; margin-bottom:10px;">
                        <h4>{a['title']}</h4>
                        <p style="color:#cbd5e1; font-size:0.9rem;">{a['source']} • {a['publishedAt'][:10]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.button(f"🔍 Analyze This", key=f"btn_{i}", on_click=go_to_analysis, args=(a['url'],))

            # Article 2
            if i + 1 < len(articles):
                with c2:
                    a = articles[i+1]
                    with st.container():
                        st.markdown(f"""
                        <div class="glass-card">
                            <img src="{a['image']}" style="width:100%; border-radius:10px; height:180px; object-fit:cover; margin-bottom:10px;">
                            <h4>{a['title']}</h4>
                            <p style="color:#cbd5e1; font-size:0.9rem;">{a['source']} • {a['publishedAt'][:10]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.button(f"🔍 Analyze This", key=f"btn_{i+1}", on_click=go_to_analysis, args=(a['url'],))

# --- HISTORY PAGE ---
elif st.session_state.active_tab == "History":
    st.markdown("### 📊 Analysis History")
    
    data = stats_manager.get_stats()
    
    if not data or not data.get('history'):
        st.info("📌 No analysis history yet. Start analyzing articles to build your history!")
    else:
        # Display total count
        st.markdown(f"**Total Articles Analyzed:** {data['total']}")
        st.markdown("---")
        
        # Reverse history to show most recent first
        history = list(reversed(data['history']))
        
        # Display each article
        for idx, record in enumerate(history):
            # Determine verdict color
            verdict = record.get('verdict', 'Unknown')
            if 'Reliable' in verdict:
                verdict_color = "#34d399"
                verdict_icon = "✅"
            elif 'Unreliable' in verdict or 'Questionable' in verdict:
                verdict_color = "#ef4444"
                verdict_icon = "❌"
            elif 'Satire' in verdict:
                verdict_color = "#facc15"
                verdict_icon = "😄"
            else:
                verdict_color = "#94a3b8"
                verdict_icon = "❓"
            
            # Create expandable card for each article
            with st.expander(f"{verdict_icon} **{verdict}** - Score: {record.get('score', 0)}/100 | {record.get('timestamp', '')[:10]}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Article snippet
                    st.markdown("#### 📄 Article Preview")
                    snippet = record.get('article_snippet', 'No preview available')
                    st.markdown(f"_{snippet}_")
                    
                    # Summary
                    st.markdown("#### 📝 AI Summary")
                    st.info(record.get('summary', 'No summary available'))
                    
                    # Key metrics
                    st.markdown("#### 🔍 Key Metrics")
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    
                    with metric_col1:
                        st.metric("Credibility Score", f"{record.get('score', 0)}/100")
                    
                    with metric_col2:
                        bias = record.get('bias', 'Unknown')
                        st.metric("Political Bias", bias)
                    
                    with metric_col3:
                        clickbait = "Yes" if record.get('is_clickbait', False) else "No"
                        st.metric("Clickbait", clickbait)
                
                with col2:
                    # Verdict badge
                    st.markdown(f"""
                    <div style="background: {verdict_color}20; border: 2px solid {verdict_color}; border-radius: 10px; padding: 1rem; text-align: center; margin-bottom: 1rem;">
                        <div style="font-size: 2rem;">{verdict_icon}</div>
                        <h3 style="color: {verdict_color}; margin: 0.5rem 0;">{verdict}</h3>
                        <p style="font-size: 2rem; font-weight: bold; margin: 0;">{record.get('score', 0)}</p>
                        <p style="font-size: 0.8rem; color: #94a3b8; margin: 0;">Credibility</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Download PDF button
                    if record.get('full_analysis') and record.get('article_full'):
                        try:
                            pdf_bytes = generate_pdf_report(
                                record.get('article_full', ''),
                                record.get('full_analysis', {})
                            )
                            st.download_button(
                                label="📄 Download Report",
                                data=pdf_bytes,
                                file_name=f"truthlens_report_{idx+1}.pdf",
                                mime="application/pdf",
                                key=f"download_history_{idx}",
                                use_container_width=True
                            )
                        except:
                            st.caption("⚠️ Report unavailable")
                    
                    # Timestamp
                    st.caption(f"🕒 {record.get('timestamp', 'Unknown')[:19]}")
                
                st.markdown("---")

# --- STATS PAGE ---
elif st.session_state.active_tab == "Stats":
    st.markdown("### 📈 Your Analysis History")
    
    data = stats_manager.get_stats()
    
    if not data:
        st.info("No analysis history found yet. Analyze some articles to see your stats!")
    else:
        # 1. Summary Cards
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <h1 style="color:#38bdf8; margin:0;">{data['total']}</h1>
                <p>Articles Analyzed</p>
            </div>
            """, unsafe_allow_html=True)
        
        with c2:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <h1 style="color:#34d399; margin:0;">{data['real']}</h1>
                <p>Reliable Content</p>
            </div>
            """, unsafe_allow_html=True)
            
        with c3:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <h1 style="color:#ef4444; margin:0;">{data['fake']}</h1>
                <p>Fake/Unreliable</p>
            </div>
            """, unsafe_allow_html=True)
            
        with c4:
             st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <h1 style="color:#facc15; margin:0;">{data['avg_score']}</h1>
                <p>Avg Credibility Score</p>
            </div>
            """, unsafe_allow_html=True)

        # 2. Charts
        sc1, sc2 = st.columns([1, 1])
        
        with sc1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 🧠 Verdict Distribution")
            
            # Donut Chart for Verdicts
            labels = ['Real', 'Fake', 'Satire']
            values = [data['real'], data['fake'], data['satire']]
            colors = ['#34d399', '#ef4444', '#facc15']
            
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker_colors=colors)])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=300, showlegend=True, margin=dict(l=20, r=20, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with sc2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📊 Bias Trends")
            
            # Bar chart for Bias from history
            counts = {'Left': 0, 'Center-Left':0, 'Center':0, 'Center-Right':0, 'Right':0}
            for rec in data['history']:
                bias = rec.get('bias', 'Center')
                if bias in counts:
                     counts[bias] += 1
                else: 
                     # Handle slight gemini variations "Center-Left" vs "Left-Center"
                     counts['Center'] += 1
            
            fig = go.Figure([go.Bar(x=list(counts.keys()), y=list(counts.values()), marker_color='#60a5fa')])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"}, height=300, margin=dict(l=20, r=20, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 3. Recent Analyses Section
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Recent Analyses")
        
        # Get last 5 analyses
        recent_analyses = list(reversed(data['history']))[:5]
        
        for idx, record in enumerate(recent_analyses):
            # Determine verdict styling
            verdict = record.get('verdict', 'Unknown')
            score = record.get('score', 0)
            
            if 'Reliable' in verdict:
                verdict_color = "#34d399"
                verdict_icon = "✅"
                percentage_label = "Reliability"
            elif 'Unreliable' in verdict or 'Questionable' in verdict:
                verdict_color = "#ef4444"
                verdict_icon = "❌"
                percentage_label = "Unreliability"
            elif 'Satire' in verdict:
                verdict_color = "#facc15"
                verdict_icon = "😄"
                percentage_label = "Satire Confidence"
            else:
                verdict_color = "#94a3b8"
                verdict_icon = "❓"
                percentage_label = "Confidence"
            
            # Create compact card
            st.markdown(f"""
            <div class="glass-card" style="padding: 1rem; margin-bottom: 1rem; border-left: 4px solid {verdict_color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                            <span style="font-size: 1.5rem;">{verdict_icon}</span>
                            <h4 style="margin: 0; color: {verdict_color};">{verdict}</h4>
                            <span style="background: {verdict_color}30; color: {verdict_color}; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.85rem; font-weight: bold;">{score}% {percentage_label}</span>
                        </div>
                        <p style="color: #94a3b8; font-size: 0.9rem; margin: 0.5rem 0; font-style: italic;">"{record.get('summary', 'No summary available')[:150]}..."</p>
                        <p style="color: #64748b; font-size: 0.8rem; margin: 0;">
                            📅 {record.get('timestamp', '')[:10]} | 
                            🎯 Bias: {record.get('bias', 'Unknown')} | 
                            {'🎣 Clickbait' if record.get('is_clickbait', False) else '✓ Trustworthy Headline'}
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # View All Button
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button("📊 View All in History", key="view_all_history", use_container_width=True, type="primary"):
                st.session_state.active_tab = "History"
                st.rerun()
