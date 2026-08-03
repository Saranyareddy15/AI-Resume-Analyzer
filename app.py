"""
AI Resume Analyzer - Stage 1-4 skeleton.

Run:
    python app.py

Before running:
    1. Create the DB: mysql -u root -p < schema.sql
    2. Update config.py (or set env vars) with your MySQL password
    3. pip install -r requirements.txt
"""

import os
from functools import wraps

from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import config
import models
from utils.pdf_parser import extract_text_from_pdf
from utils.analyzer import compute_ats_score

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH

os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


# ---------- Auth ----------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]

        if not username or not email or not password:
            flash("All fields are required.")
            return redirect(url_for("register"))

        if models.get_user_by_username(username):
            flash("Username already taken.")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)
        user_id = models.create_user(username, email, password_hash)
        session["user_id"] = user_id
        session["username"] = username
        flash("Account created!")
        return redirect(url_for("dashboard"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        user = models.get_user_by_username(username)
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- Core app ----------

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    history = models.get_history_for_user(session["user_id"])
    return render_template("dashboard.html", history=history, username=session["username"])


@app.route("/analyze", methods=["GET", "POST"])
@login_required
def analyze():
    if request.method == "POST":
        resume_file = request.files.get("resume")
        jd_text = request.form.get("job_description", "").strip()
        job_title = request.form.get("job_title", "Untitled role").strip()

        if not resume_file or resume_file.filename == "":
            flash("Please upload a resume PDF.")
            return redirect(url_for("analyze"))

        if not allowed_file(resume_file.filename):
            flash("Only PDF files are supported.")
            return redirect(url_for("analyze"))

        if not jd_text:
            flash("Please paste the job description.")
            return redirect(url_for("analyze"))

        filename = secure_filename(resume_file.filename)
        resume_text = extract_text_from_pdf(resume_file.stream)

        result = compute_ats_score(resume_text, jd_text)

        models.save_analysis(
            user_id=session["user_id"],
            resume_filename=filename,
            job_title=job_title,
            ats_score=result["score"],
            matched=result["matched"],
            missing=result["missing"],
        )

        return render_template(
            "result.html",
            filename=filename,
            job_title=job_title,
            result=result,
        )

    return render_template("analyze.html")


if __name__ == "__main__":
    app.run(debug=True)
