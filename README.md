# 🦅 TruthLens AI

> **Detect Fake News with AI Precision.**  
> _A Hybrid Intelligence System combining Local Machine Learning (99% Accuracy) with Large Language Model Reasoning (Google Gemini) to fight misinformation in real-time._

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fakenewsdetectiongit-otound4iovj5xrejuzwrvl2.streamlit.app/)
![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)
![License MIT](https://img.shields.io/badge/license-MIT-green)

---

## 🌍 impact & Purpose

In an era of information overload, **TruthLens AI** serves as a critical digital defense system. Misinformation spreads 6x faster than truth on social media. This tool empowers users to verify information instantly, fostering a more informed and resilient society.

### 📊 Key Performance Metrics
| Metric | Value | Description |
| :--- | :--- | :--- |
| **Detection Accuracy** | **99.2%** | Achieved by our localized PassiveAggressive Classifier on the standard fake news dataset. |
| **Analysis Depth** | **5+ Dimensions** | Evaluates Factuality, Political Bias, Logical Fallacies, Sensationalism, and Emotional Tone. |
| **Response Time** | **< 2.5s** | Real-time verification capabilities for instant decision making. |
| **Bias Sensitivity** | **High** | Capable of detecting subtle political leans (Left, Center, Right) often missed by standard classifiers. |

---

## ✨ Key Features

*   **🧠 Hybrid Intelligence Engine**:
    *   **Layer 1 (Speed):** Local ML Model (Scikit-Learn) for instant "True/Fake" classification.
    *   **Layer 2 (Depth):** Gemini AI (Google) for explaining *why* a story is fake, identifying logical fallacies, and checking facts against world knowledge.
*   **🎣 Clickbait Detector**: Calculates a "Dissonance Score" to measure the gap between a sensational headline and the actual article content.
*   **🕸️ Bias Radar**: unique visualization plotting Subjectivity, Sensationalism, and Partisanship.
*   **📡 Live Verification**: Fetches real-time trending global news to analyze stories as they break (uses NewsAPI).
*   **📄 Professional Reporting**: Generates downloadable PDF certification reports for any analyzed article—perfect for journalists and researchers.
*   **📈 Personal Dashboard**: Tracks your history and verification statistics over time.

---

## 🛠️ Tech Stack

*   **Frontend**: [Streamlit](https://streamlit.io/) (Custom CSS for Glassmorphism UI)
*   **AI/LLM**: [Google Gemini 1.5 Flash](https://ai.google.dev/)
*   **Machine Learning**: Scikit-Learn (TF-IDF Vectorization, PassiveAggressive Classifier)
*   **Data Processing**: Pandas, NumPy, NLTK
*   **Visualization**: Plotly Interactive Charts
*   **News Aggregation**: NewsAPI
*   **Utilities**: FPDF (Report Generation), BeautifulSoup (Web Scraping)

---

## 🚀 Installation & Setup

Clone the repository and run the application locally.

### 1. Clone the Repo
```bash
git clone https://github.com/YOUR_USERNAME/FakeNewsDetection.git
cd FakeNewsDetection
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Secrets
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY="your_gemini_api_key_here"
NEWS_API_KEY="your_news_api_key_here"
```

### 5. Run the App
```bash
streamlit run app.py
```

---

## 📸 Screenshots

| Dashboard | Analysis Results |
| :---: | :---: |
| _Hero Section & Features_ | _Deep Dive Analysis & Graphs_ |

---

## 🤝 Contributing

We welcome contributions!
1.  **Fork** the project.
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the Branch (`git push origin feature/AmazingFeature`).
5.  Open a **Pull Request**.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">Made with ❤️ for Truth & Transparency</p>
