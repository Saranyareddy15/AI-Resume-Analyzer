"""
Thin data-access layer. Each function opens its own connection and
closes it — simple and safe for a beginner project (a connection
pool is a nice upgrade later, not needed to get started).
"""

import mysql.connector
from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ---------- Users ----------

def create_user(username, email, password_hash):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
        (username, email, password_hash),
    )
    conn.commit()
    user_id = cur.lastrowid
    cur.close()
    conn.close()
    return user_id


def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


# ---------- Analysis history ----------

def save_analysis(user_id, resume_filename, job_title, ats_score, matched, missing):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO analysis_history
           (user_id, resume_filename, job_title, ats_score, matched_keywords, missing_keywords)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (user_id, resume_filename, job_title, ats_score,
         ",".join(matched), ",".join(missing)),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_history_for_user(user_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM analysis_history WHERE user_id = %s ORDER BY created_at DESC",
        (user_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
