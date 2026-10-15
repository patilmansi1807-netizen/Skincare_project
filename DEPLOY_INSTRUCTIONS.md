# 🌐 How to Share Your "GlowCare" Website Online

You have **two easy ways** to share your project with anyone:

---

## 🚀 Option 1: Instant Public Share Link (Ready in 5 Seconds)

We have created an automated launcher that turns your local Flask app into a live public HTTPS website link that anyone in the world can open on their mobile phone or PC.

### How to use:

1. Double-click the file: **[`share_website.bat`](file:///c:/Users/mansi/OneDrive/Desktop/skincare/share_website.bat)**  
   *(or open your terminal and run: `python share_website.py`)*
2. It will generate your public live link:
   👉 **`https://glowcare-app.loca.lt`**
3. Share that link with your friends, professors, or evaluators!

*(Note: When someone opens a `.loca.lt` link for the first time, it might ask for the "Tunnel Password". The script will automatically display your IP in the console to copy and paste.)*

---

## ☁️ Option 2: Permanent 24/7 Free Cloud Hosting (Live Forever)

If you want your website to stay online 24/7 without needing your computer turned on, you can deploy it to **Render.com** for free:

### Quick 3-Step Deployment on Render:

1. **Push to GitHub**:
   - Create a GitHub repository (e.g., `glowcare-skincare`).
   - Push your project files to GitHub.
2. **Open Render**:
   - Go to [https://render.com](https://render.com) and sign in for free with GitHub.
   - Click **New +** -> **Web Service**.
   - Select your GitHub repository.
3. **Configure & Deploy**:
   - **Name**: `glowcare` (or your chosen project name)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - Click **Create Web Service**.

🎉 Your permanent website will be live at:
👉 **https://glowcare.onrender.com/`**
