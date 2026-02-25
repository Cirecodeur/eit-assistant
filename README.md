# 🤖 EIT AI Assistant

An advanced AI-powered assistant built by **EIT** to simplify information consumption. This application can summarize long-form articles from the web or extract and synthesize content from uploaded PDF documents.

---

## 🔗 Live Application

**Deployed URL:** [PASTE_YOUR_FLY_IO_LINK_HERE]

---

## ✨ Features

- **Link Summarization 🔗**: Automatically fetches and cleans text from web articles.
- **PDF Analysis 📄**: Parses uploaded PDF files to extract core information.
- **EIT Persona**: Integrated identity and professional tone (same as the creator: EIT).
- **Smart Export**: Generate and download a PDF version of the AI's summary.
- **Reliability**: Built-in graceful exception handling for broken links or API issues.
- **Traceability**: Comprehensive logging system tracking application flow in `app.log`.

---

## 🛠️ Technical Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI Engine**: [Google Gemini 1.5 Flash](https://ai.google.dev/)
- **Scraping**: BeautifulSoup4 & Requests
- **PDF Processing**: PyPDF2 (Reading) & FPDF2 (Generation)
- **Hosting**: [Fly.io](https://fly.io/) (Containerized with Docker)

---

## 🚀 Installation & Local Setup

Follow these steps to run the assistant on your local machine:

### 1. Clone the repository

```bash
git clone <your-github-repo-url>
cd eit-assistant



# Create the environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (macOS/Linux)
source venv/bin/activate



3. Install dependencies
pip install -r requirements.txt


streamlit run app.py



☁️ Deployment on Fly.io

This application is configured for Fly.io. To deploy:

    Initialize: fly launch (Fly will automatically detect the Dockerfile).

    Set Secrets:

    ---
    ->fly secrets set GOOGLE_API_KEY=your_actual_key_here

    ->fly deploy

### Rappel de dernière minute 💡 :
Avant de fermer ton projet, assure-toi que ton dépôt GitHub contient bien ces **5 fichiers** à la racine :
1. `app.py`
2. `requirements.txt`
3. `Dockerfile`
4. `.gitignore`
5. `README.md` (celui-ci !)

**C'est dans la boîte ! Veux-tu que je t'explique comment vérifier une dernière fois que Fly.io a bien pris tes logs en compte ?**
```
