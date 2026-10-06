# AI-Powered Fake News Detection & Analytics Platform

A professional full-stack Data Science & Machine Learning platform built using Python, Flask, Scikit-learn, TF-IDF Vectorization, SQLite, React, and Tailwind CSS.

---

## 🌟 Key Features

- **Authentication & User Management**:
  - Secure Login, Registration, Forgot Password, and Reset Password flows.
  - PBKDF2:SHA256 password hashing & token session management.
  - Role-Based Access Control (**`USER` vs `ADMIN`**).
  - Admin Dashboard with User Directory, Role Promotion/Demotion, and Account Deletion.
  - User Profile page with personal statistics, profile editing, and password change modals.
- **NLP & Machine Learning Engine**: 
  - Complete preprocessing pipeline (lowercasing, punctuation & URL removal, tokenization, stop-words filtering, stemming/lemmatization).
  - TF-IDF Vectorization with unigrams & bigrams.
  - Multi-model evaluation pipeline comparing **Logistic Regression**, **Multinomial Naive Bayes**, and **Linear Support Vector Machine (Linear SVM)**.
  - Auto-selects best model based on F1 Score and saves binaries (`model.pkl` & `vectorizer.pkl`).
- **Interactive Analytics Dashboard**:
  - 7 KPI summary cards (Total Checked, Real Count, Fake Count, Accuracy, Precision, Recall, F1 Score).
  - Donut Chart (Real vs Fake distribution).
  - Line Chart (Predictions over time).
  - 2x2 Confusion Matrix grid (TP, TN, FP, FN).
  - Comparative Model Performance Table.
- **Exploratory Dataset Analytics**:
  - Dynamic dataset statistics (records, missing values, duplicates, class distribution, top word frequencies, and live sample preview).

---

## 🔑 Pre-seeded Demo Credentials

| Role | Email / Username | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin@veritruth.ai` or `admin` | `Admin@123` | Admin Dashboard, User Management, Detector, Dataset Insights, ML Pipeline, Profile |
| **User** | `user@veritruth.ai` or `demouser` | `User@123` | Detector, Analytics Dashboard, Prediction History, Dataset Insights, Profile |

---

## 🛠️ Quick Start Guide

```bash
# 1. Activate virtual environment
.\.venv\Scripts\activate

# 2. Run Flask application
python backend/app.py
```

Access Web App in browser: **`http://127.0.0.1:5000/`**

---

## 📡 REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/auth/register` | User registration with input validation. |
| `POST` | `/api/auth/login` | User login against PBKDF2 hashed password. |
| `GET` | `/api/auth/me` | Fetches active user details and personal stats. |
| `PUT` | `/api/auth/profile` | Updates full name & email. |
| `PUT` | `/api/auth/change-password` | Updates password after verifying current hash. |
| `POST` | `/api/auth/forgot-password` | Generates secure password reset token. |
| `POST` | `/api/auth/reset-password` | Resets password with valid reset token. |
| `GET` | `/api/admin/stats` | System-wide statistics for Admin. |
| `GET` | `/api/admin/users` | List of all registered user accounts. |
| `PUT` | `/api/admin/users/<id>/role` | Promote/demote user role (`user` ↔ `admin`). |
| `DELETE`| `/api/admin/users/<id>` | Deletes user account. |
| `POST` | `/api/predict` | Classifies input text as `Likely Real` or `Likely Fake`. |
| `GET` | `/api/dashboard` | Serves KPI cards, timeline, and model comparison metrics. |
| `GET` | `/api/history` | Fetches prediction history. |
| `GET` | `/api/dataset-stats` | Training set statistics & top word frequencies. |
| `GET` | `/api/model-performance` | Comprehensive ML model evaluation metrics. |
