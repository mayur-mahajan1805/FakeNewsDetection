from fpdf import FPDF
import datetime

def safe_encode(text):
    """
    Sanitizes text to be compatible with FPDF (Latin-1).
    Replaces common smart quotes/dashes and strips unsupported chars.
    """
    if not isinstance(text, str): return str(text)
    
    replacements = {
        "\u201c": '"', "\u201d": '"',  # Smart quotes
        "\u2018": "'", "\u2019": "'",  # Smart single quotes
        "\u2013": "-", "\u2014": "-",  # Dashes
        "\u2026": "..."                # Ellipsis
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
        
    # Final strip of anything not in latin-1
    return text.encode('latin-1', 'replace').decode('latin-1')

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'TruthLens AI - Credibility Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf_report(article_text, analysis):
    pdf = PDFReport()
    pdf.add_page()
    
    # Title & Timestamp
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'R')
    pdf.ln(5)
    
    # 1. Verification Section
    pdf.set_font("Arial", 'B', 16)
    
    if "Reliable" in analysis.get('classification', 'Unreliable'):
        pdf.set_text_color(34, 197, 94)
    else:
        pdf.set_text_color(239, 68, 68)
        
    pdf.cell(0, 10, safe_encode(f"Verdict: {analysis.get('classification', 'Unknown').upper()}"), 0, 1, 'L')
    pdf.set_text_color(0, 0, 0) # Reset
    
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, safe_encode(f"Credibility Score: {analysis.get('credibility_score', 0)}/100"), 0, 1, 'L')
    pdf.ln(5)
    
    # 2. Executive Summary
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Executive Summary", 0, 1, 'L')
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, safe_encode(analysis.get('summary', 'No summary provided.')))
    pdf.ln(5)
    
    # 3. Detailed Metrics
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Detailed Analysis", 0, 1, 'L')
    pdf.set_font("Arial", size=11)
    
    bias = analysis.get('bias_analysis', {})
    pdf.cell(0, 7, safe_encode(f"Political Bias: {bias.get('political_spectrum', 'N/A')}"), 0, 1)
    pdf.cell(0, 7, safe_encode(f"Emotional Tone: {bias.get('emotional_tone', 'N/A')}"), 0, 1)
    pdf.cell(0, 7, safe_encode(f"Sensationalism Rating: {analysis.get('sensationalism_rating', 'N/A')}/100"), 0, 1)
    
    clickbait = analysis.get('clickbait_analysis', {})
    is_cb = "Yes" if clickbait.get('is_clickbait') else "No"
    pdf.cell(0, 7, safe_encode(f"Clickbait Detected: {is_cb} (Dissonance: {clickbait.get('dissonance_score', 0)}%)"), 0, 1)
    pdf.ln(5)
    
    # 4. Logical Fallacies
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Logical Fallacies / Red Flags", 0, 1, 'L')
    pdf.set_font("Arial", size=11)
    fallacies = analysis.get('fallacies', [])
    if fallacies:
        for f in fallacies:
            pdf.cell(0, 7, safe_encode(f"- {f}"), 0, 1)
    else:
        pdf.cell(0, 7, "No major logical fallacies detected.", 0, 1)
    pdf.ln(10)
    
    # 5. Article Text Snapshot
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Analyzed Article Text (Snippet)", 0, 1, 'L')
    pdf.set_font("Courier", size=10)
    
    full_text = article_text[:2000] + "..." if len(article_text) > 2000 else article_text
    pdf.multi_cell(0, 5, safe_encode(full_text))
    
    # Return bytes safely
    return pdf.output(dest='S').encode('latin-1')
