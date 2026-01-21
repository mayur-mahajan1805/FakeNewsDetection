# TruthLens AI - Testing URLs Guide

## Test Articles for Different Categories

### ✅ **Reliable News Sources**

#### 1. BBC News (Highly Reliable)
```
https://www.bbc.com/news/world
https://www.bbc.com/news/technology
https://www.bbc.com/news/science-environment
```
**Expected Result**: 
- Verdict: Reliable
- Score: 85-95%
- Bias: Center/Center-Left
- Clickbait: No

#### 2. Reuters (Highly Reliable)
```
https://www.reuters.com/world/
https://www.reuters.com/technology/
```
**Expected Result**:
- Verdict: Reliable
- Score: 90-100%
- Bias: Center
- Clickbait: No

#### 3. Associated Press (AP)
```
https://apnews.com/
```
**Expected Result**:
- Verdict: Reliable
- Score: 90-95%
- Bias: Center
- Clickbait: No

#### 4. NPR (Reliable)
```
https://www.npr.org/sections/news/
```
**Expected Result**:
- Verdict: Reliable
- Score: 80-90%
- Bias: Center-Left
- Clickbait: No

---

### 😄 **Satire News (Should Detect as Satire)**

#### 1. The Onion (Classic Satire)
```
https://www.theonion.com/
https://www.theonion.com/nation
```
**Expected Result**:
- Verdict: Satire
- Score: 20-40%
- Clickbait: Often Yes
- Note: Should identify satirical language

#### 2. The Babylon Bee (Conservative Satire)
```
https://babylonbee.com/
```
**Expected Result**:
- Verdict: Satire
- Score: 30-50%
- Clickbait: Often Yes

#### 3. The Borowitz Report (New Yorker Satire)
```
https://www.newyorker.com/humor/borowitz-report
```
**Expected Result**:
- Verdict: Satire
- Score: 40-60%
- More subtle satire

---

### ❌ **Questionable/Unreliable Sources**

#### 1. Natural News (Known for Misinformation)
```
https://www.naturalnews.com/
```
**Expected Result**:
- Verdict: Unreliable/Questionable
- Score: 10-30%
- Bias: Far-Right
- Sensationalism: High

#### 2. InfoWars (Conspiracy Theories)
```
https://www.infowars.com/
```
**Expected Result**:
- Verdict: Unreliable
- Score: 5-20%
- Bias: Far-Right
- Sensationalism: Very High

---

### 🎣 **Clickbait Testing**

#### 1. BuzzFeed (Clickbait Style)
```
https://www.buzzfeed.com/
```
**Expected Result**:
- Verdict: Questionable (for news) / Reliable (for entertainment)
- Clickbait: Often Yes
- Sensationalism: Medium-High

#### 2. Upworthy (Clickbait Headlines)
```
https://www.upworthy.com/
```
**Expected Result**:
- Clickbait: Yes
- Headline-Body Dissonance: Possible

---

### 🧪 **Mixed/Educational Testing**

#### 1. Wikipedia (Neutral, Factual)
```
https://en.wikipedia.org/wiki/Artificial_intelligence
https://en.wikipedia.org/wiki/Climate_change
```
**Expected Result**:
- Verdict: Reliable
- Score: 75-85%
- Bias: Center
- Clickbait: No

#### 2. Scientific American (Science Journalism)
```
https://www.scientificamerican.com/
```
**Expected Result**:
- Verdict: Reliable
- Score: 85-95%
- Bias: Center-Left
- Clickbait: No

#### 3. The Guardian (Left-Leaning)
```
https://www.theguardian.com/international
```
**Expected Result**:
- Verdict: Reliable
- Score: 75-85%
- Bias: Left/Center-Left
- Clickbait: Occasional

#### 4. Fox News (Right-Leaning)
```
https://www.foxnews.com/
```
**Expected Result**:
- Verdict: Questionable/Reliable (varies)
- Score: 60-75%
- Bias: Right/Center-Right
- Clickbait: Occasional

---

## Testing Strategy

### 1. **Baseline Testing** (Start Here)
Test these in order to understand the system:
1. BBC article (Reliable baseline)
2. The Onion article (Satire baseline)
3. Wikipedia article (Neutral baseline)

### 2. **Edge Case Testing**
- Opinion pieces vs news articles
- Breaking news vs in-depth analysis
- Local news vs international news

### 3. **Bias Detection Testing**
Compare articles from:
- Left-leaning: The Guardian, NPR
- Center: Reuters, AP
- Right-leaning: Fox News, Wall Street Journal

### 4. **Clickbait Testing**
- BuzzFeed listicles
- Viral news sites
- Social media shared articles

---

## Sample Test Articles (Copy-Paste Ready)

### Reliable News
```
https://www.bbc.com/news/technology-68000000
https://www.reuters.com/world/
https://apnews.com/
```

### Satire
```
https://www.theonion.com/
https://babylonbee.com/
```

### Educational
```
https://en.wikipedia.org/wiki/Machine_learning
https://www.scientificamerican.com/
```

---

## What to Look For

### ✅ Good Detection Signs
- Reliable sources score 80-100%
- Satire is identified correctly
- Bias is detected accurately
- Clickbait headlines are flagged

### ⚠️ Areas to Monitor
- Opinion pieces might score lower (expected)
- Breaking news might have less context
- Paywalled articles might not scrape fully

### 🔍 Testing Checklist
- [ ] Test at least 3 reliable sources
- [ ] Test at least 2 satire sources
- [ ] Test 1 known unreliable source
- [ ] Test clickbait headlines
- [ ] Test different political biases
- [ ] Download PDF reports
- [ ] Check History tab
- [ ] Verify Stats dashboard

---

## Notes

### Scraping Limitations
Some sites may block scraping:
- Use the "Paste Text" option if scraping fails
- Copy article text manually from browser
- Test with publicly accessible articles

### API Rate Limits
- Gemini API: 15 requests/minute (free tier)
- NewsAPI: 100 requests/day (free tier)
- Space out tests if hitting limits

### Best Practices
1. Start with reliable sources to calibrate
2. Test satire to verify detection
3. Mix different bias levels
4. Check both URL and text paste methods
5. Review PDF reports for completeness

---

**Happy Testing! 🧪🔍**
