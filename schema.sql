-- Run this once to set up the database:
--   mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS resume_analyzer;
USE resume_analyzer;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS analysis_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    resume_filename VARCHAR(255),
    job_title VARCHAR(255),
    ats_score FLOAT NOT NULL,
    matched_keywords TEXT,
    missing_keywords TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
