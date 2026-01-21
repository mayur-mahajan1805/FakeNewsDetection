# How to Deploy TruthLens AI to Streamlit Cloud

Follow these steps to deploy your application to the web for free using Streamlit Community Cloud.

## Prerequisite: GitHub Repository
Streamlit Cloud deploys directly from GitHub.

1. **Create a GitHub Repository**
   - Go to [GitHub.com/new](https://github.com/new).
   - Name it `truth-lens-ai`.
   - Select **Public** (easier for free deployment) or Private.
   - Click **Create repository**.

2. **Push Your Code**
   Open your terminal in the project folder and run:
   ```bash
   # Initialize git if you haven't already
   git init
   
   # Add all files (make sure .env is in .gitignore!)
   git add .
   
   # Commit
   git commit -m "Initial commit for TruthLens AI"
   
   # Link to your new GitHub repo (replace YOUR_USERNAME)
   git remote add origin https://github.com/YOUR_USERNAME/truth-lens-ai.git
   
   # Push
   git branch -M main
   git push -u origin main
   ```

## Step 1: Sign up for Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Click **Sign up** and choose **Continue with GitHub**.
3. Authorize Streamlit to access your repositories.

## Step 2: Deploy the App
1. Once logged in, click the **"New app"** button (top right).
2. FIll in the details:
   - **Repository**: Select `YOUR_USERNAME/truth-lens-ai`.
   - **Branch**: `main`.
   - **Main file path**: `app.py`.
3. Click **Deploy!**

## Step 3: Configure API Keys (IMPORTANT)
Your app will fail initially because the API keys (Gemini & NewsAPI) are hidden in your local `.env` file, which is not uploaded to GitHub for security. You must add them to Streamlit's "Secrets".

1. On your deployed app screen, click the **Manage App** button (bottom right) or the **three dots menu (⋮)** on the top right -> **Settings**.
2. Go to the **Secrets** tab.
3. Paste your keys in the TOML format shown below:

```toml
GEMINI_API_KEY = "Your_Gemini_Key_Here"
NEWS_API_KEY = "Your_News_Key_Here"
```
*(Copy the actual keys from your local `.env` file)*

4. Click **Save**.

## Step 4: Restart
The app should automatically detect the new secrets and restart. If not, click **Reboot** in the Manage App menu.

---
**Your app is now live!** You can share the URL (e.g., `https://truth-lens-ai.streamlit.app`) with anyone.
