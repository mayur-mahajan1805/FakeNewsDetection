# Satire Detection in TruthLens AI

## How Satire Detection Works

### 🧠 **Detection Mechanism**

TruthLens AI uses a **hybrid approach** to detect satire:

#### 1. **Local ML Model (First Pass)**
- Trained on Kaggle dataset (Fake.csv + True.csv)
- Looks for linguistic patterns
- **Limitation**: May not distinguish satire from fake news
- Usually classifies satire as "FAKE" (which is technically correct for credibility)

#### 2. **Gemini AI (Deep Analysis)**
- Analyzes context, tone, and intent
- Looks for satirical markers:
  - Absurd exaggeration
  - Ironic language
  - Humorous intent
  - Parody elements
  - Known satire sources (The Onion, Babylon Bee)
- **Smart enough** to distinguish satire from malicious fake news

### 🎯 **Chain-of-Thought Analysis**

The Gemini prompt specifically asks:
```
"Is this satire/parody or genuine misinformation?"
```

It considers:
1. **Source credibility** (Is it from The Onion?)
2. **Language patterns** (Absurd claims, humor)
3. **Intent** (To entertain vs to deceive)
4. **Context** (Obvious exaggeration vs subtle lies)

---

## 📊 **Expected Output for Satire**

### ✅ **Ideal Satire Detection**

When analyzing a satire article (e.g., The Onion), you should see:

#### **Verdict Section:**
```
Classification: Satire
Credibility Score: 20-40%
```

#### **Visual Indicators:**
- 😄 **Yellow/Gold color** (not red for fake)
- **"Satire" badge** prominently displayed
- **Lower credibility score** (20-40%) because it's not factual

#### **Executive Summary:**
```
"This article appears to be satirical content from a known 
parody news source. While the claims are false, the intent 
is humor and social commentary rather than deception."
```

#### **Bias Analysis:**
```
Political Spectrum: Varies (depends on satire target)
Emotional Tone: Humorous/Ironic
Sensationalism Rating: High (intentional for comedic effect)
```

#### **Clickbait Analysis:**
```
Is Clickbait: Often Yes
Dissonance Score: High
Reason: "Satirical headlines are designed to be absurd 
and attention-grabbing for comedic effect"
```

#### **Logical Fallacies:**
```
- Intentional exaggeration for comedic effect
- Absurd premises (part of satire format)
- Note: These are features, not bugs, of satire
```

---

## 🔍 **Real-World Examples**

### **Example 1: The Onion Article**

**Input:**
```
Title: "Nation's Dog Owners Demand To Know Who's A Good Boy"
Source: theonion.com
```

**Expected Output:**
```
✅ Classification: Satire
📊 Score: 25%
😄 Icon: Yellow badge
📝 Summary: "Satirical article from The Onion using absurd 
            premise for humor. Not intended as factual news."
🎯 Bias: Center (satirizing general culture)
🎣 Clickbait: Yes (intentional for comedy)
```

### **Example 2: Babylon Bee Article**

**Input:**
```
Title: "Local Man's Beard Reaches Sentience, Demands Voting Rights"
Source: babylonbee.com
```

**Expected Output:**
```
✅ Classification: Satire
📊 Score: 30%
😄 Icon: Yellow badge
📝 Summary: "Conservative satire site article with absurd 
            premise. Clearly fictional for comedic purposes."
🎯 Bias: Right (conservative satire)
🎣 Clickbait: Yes (humorous exaggeration)
```

---

## ⚠️ **Potential Issues & Solutions**

### **Issue 1: Satire Classified as "Unreliable"**
**Why it happens:**
- Local ML model sees false claims
- Gemini might be overly cautious

**What to look for:**
- Check the **summary** - it should mention "satire" or "parody"
- Look at **source** - known satire sites should be flagged
- **Fallacies section** might note "intentional exaggeration"

**Solution:**
- The classification might say "Unreliable" but summary should clarify it's satire
- This is actually acceptable since satire IS unreliable as factual news

### **Issue 2: Subtle Satire Missed**
**Why it happens:**
- Some satire is very subtle (e.g., The Borowitz Report)
- AI might not catch sophisticated parody

**What to look for:**
- Lower credibility score (50-70%)
- Summary might mention "questionable claims"
- May not explicitly say "satire"

**Solution:**
- This is a known limitation
- Obvious satire (The Onion) should always be caught
- Subtle satire might need human judgment

---

## 🎨 **Visual Output in TruthLens AI**

### **Stats Tab:**
```
📊 Verdict Distribution Chart:
- Real: Green slice
- Fake: Red slice
- Satire: Yellow slice ← Should show satire separately
```

### **History Tab:**
```
😄 Satire - Score: 30/100 | 2026-01-20
├─ Article Preview: "Nation's Dog Owners..."
├─ AI Summary: "Satirical content from The Onion..."
├─ Metrics: Satire Confidence: 30%
└─ Download Report: ✅ Available
```

### **Recent Analyses (Stats):**
```
😄 Satire
30% Satire Confidence ← Special label for satire
"Satirical article from The Onion using absurd premise..."
📅 2026-01-20 | 🎯 Bias: Center | ✓ Trustworthy Headline
```

---

## 🧪 **Testing Satire Detection**

### **Test Cases:**

#### **1. Obvious Satire (Should Always Work)**
```
Source: The Onion, Babylon Bee
Expected: Classification = "Satire", Score = 20-40%
```

#### **2. Subtle Satire (May Vary)**
```
Source: The Borowitz Report, Reductress
Expected: Classification = "Questionable" or "Satire", Score = 40-60%
```

#### **3. Not Satire (Control Test)**
```
Source: BBC, Reuters
Expected: Classification = "Reliable", Score = 85-95%
```

---

## 📋 **Satire Detection Checklist**

When analyzing satire, verify:

- [ ] **Classification** includes "Satire" or mentions it in summary
- [ ] **Score** is low (20-50%) - not factual
- [ ] **Icon** is 😄 (yellow/gold), not ❌ (red)
- [ ] **Summary** mentions "satirical," "parody," or "humor"
- [ ] **Source** is identified (The Onion, Babylon Bee, etc.)
- [ ] **Intent** is noted as "entertainment" not "deception"
- [ ] **Stats chart** shows satire as separate category (yellow)

---

## 💡 **Key Takeaways**

### **What Satire Detection Should Do:**
✅ Identify obvious satire sources (The Onion, Babylon Bee)
✅ Distinguish satire from malicious fake news
✅ Note humorous/ironic intent in summary
✅ Show low credibility score (it's not factual)
✅ Display with yellow/gold color (not red)

### **What It Won't Do:**
❌ Catch 100% of subtle satire
❌ Guarantee perfect classification every time
❌ Understand cultural context of all parody

### **Bottom Line:**
Satire detection works by recognizing:
1. **Known satire sources**
2. **Absurd/exaggerated claims**
3. **Humorous intent**
4. **Lack of factual accuracy**

The output should clearly indicate "Satire" and explain it's intentional fiction for comedy, not malicious deception.

---

**Status**: Satire detection is functional and should work for major satire sites! 🎭
