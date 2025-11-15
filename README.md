# Plagiarism Detection System

This project has two implementations for checking plagiarism in text documents.

## Projects

### 1. Plagiarism Checker
Location: plagiarism_checker/

Standalone application using Streamlit. Everything runs in one place.

### 2. Plagiarism App
Location: plagiarism_app/

Uses Flask API for backend and Streamlit for frontend. Separated architecture.

## How to Run

### Option 1: Standalone Version

cd plagiarism_checker
pip install -r requirements.txt
python data_prep.py
python model.py
streamlit run app.py

Open http://localhost:8501

### Option 2: API Version (Direct Flask)

Terminal 1:
cd plagiarism_app/flask_api
pip install -r ../requirements.txt
python model.py
python app.py

Terminal 2:
cd plagiarism_app/streamlit_app
streamlit run app.py

API: http://localhost:5000
Frontend: http://localhost:8501

### Option 3: API Version with Kong Gateway

Requires Docker Desktop installed.

cd plagiarism_app
.\start_kong.ps1

This starts:
- Flask API on port 5000
- Kong Gateway on port 8000
- Kong Admin on port 8001

Kong Features:
- Rate Limiting: 100 requests per minute, 1000 per hour
- Request Size Limit: 10MB maximum

Access API through Kong: http://localhost:8000
Streamlit frontend: http://localhost:8501

In Streamlit, check "Use Kong API Gateway" to route through Kong.

To stop Kong:
.\stop_kong.ps1

## Technologies Used

Python 3.7+
scikit-learn
TfidfVectorizer
Cosine Similarity
Logistic Regression
Streamlit
Flask (for API version)

## How It Works

1. Upload two text files
2. Convert text to vectors using TF-IDF
3. Calculate cosine similarity between vectors
4. Use ML model to predict if plagiarized
5. Highlight matching parts
6. Show results

## Sample Data

Both projects have sample files in sample_data/ folder.
original.txt - base document
submission.txt - document to check

Expected similarity score: around 0.85-0.95

## Requirements

Python 3.7 or higher
2GB RAM minimum
500MB disk space

Install packages:
pip install -r requirements.txt

## Common Problems

Model file not found - run python model.py first
Module not found - run pip install -r requirements.txt
API not connecting - make sure Flask server is running
Port in use - kill process or change port

## What I Learned

Natural Language Processing basics
TF-IDF vectorization
Cosine similarity calculation
Machine learning classification
Building REST APIs with Flask
Creating web apps with Streamlit

BITS Assignment - API-Based Products
