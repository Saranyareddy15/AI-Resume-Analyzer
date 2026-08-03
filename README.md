# AI Resume Analyzer — Starter Project

A Flask + MySQL web app that scores a resume's ATS compatibility against a job description.
This is **Stage 1–4** of the roadmap (upload, keyword-based scoring, MySQL persistence, auth).
Deep-learning-based similarity (TensorFlow) is the natural next stage — see "Next Steps" below.

## What's included

```
resume-analyzer/
├── app.py               # Flask routes (auth, upload, analysis, dashboard)
├── config.py             # DB + app settings
├── models.py             # MySQL queries (users, analysis history)
├── schema.sql             # Database schema
├── requirements.txt
├── utils/
│   ├── pdf_parser.py     # Extracts text from uploaded PDF resumes
│   └── analyzer.py       # Keyword extraction + ATS scoring logic
├── templates/            # HTML pages (Jinja2)
└── static/style.css      # Basic styling
```

## Setup (step by step)

### 1. Install MySQL (if you haven't)
Make sure a MySQL server is running locally and you know your root password.

### 2. Create the database
```bash
mysql -u root -p < schema.sql
```
This creates the `resume_analyzer` database with `users` and `analysis_history` tables.

### 3. Set up a Python virtual environment
```bash
cd resume-analyzer
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure your database password
Open `config.py` and update `DB_CONFIG["password"]` to your MySQL root password
(or set it via an environment variable: `export DB_PASSWORD=yourpassword`).

### 5. Run the app
```bash
python app.py
```
Visit **http://127.0.0.1:5000** — you'll be redirected to register/log in.

## How it works right now

1. You register/log in (password hashed with Werkzeug, stored in MySQL).
2. On "New Analysis", you upload a resume PDF and paste a job description.
3. `pdf_parser.py` extracts the resume text.
4. `analyzer.py` matches both texts against a curated skills list (`COMMON_SKILLS`),
   then computes `matched_skills / total_JD_skills * 100` as the ATS score.
5. The result — plus matched/missing skills — is saved to `analysis_history` and shown to you.
6. Your dashboard lists every past analysis.

## Next steps (to go from "working" to "portfolio-strong")

- **Better skill extraction**: replace the fixed `COMMON_SKILLS` list with a bigger skills
  taxonomy, or use spaCy's NER / noun-phrase chunking to catch skills you didn't hardcode.
- **Semantic scoring**: swap the exact keyword match in `analyzer.py` for embedding similarity
  (e.g. TensorFlow/Sentence-Transformers) so "ML" and "Machine Learning" count as the same thing.
- **Resume improvement suggestions**: turn `missing` skills into templated suggestions
  ("Consider adding a project or bullet point mentioning **Docker**").
- **REST API layer**: expose `/api/analyze` returning JSON, so this could power a
  separate frontend (React) later — matches the "REST APIs" line in your project description.
- **Deployment**: containerize with Docker, deploy to Render/Railway (free tiers work fine).

## Troubleshooting

- **`Access denied for user 'root'@'localhost'`** → your `DB_PASSWORD` in `config.py` is wrong.
- **`Unknown database 'resume_analyzer'`** → you skipped step 2 (run `schema.sql`).
- **PDF text comes back empty** → some PDFs are scanned images, not real text; `pdfplumber`
  can't extract text from those without OCR. Test with a text-based PDF resume first.
