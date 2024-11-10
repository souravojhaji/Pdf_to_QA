# Pdf_to_QA

## Overview
A full-stack application for uploading PDFs, asking questions on PDF content, and receiving AI-generated answers.

## Technologies
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: React.js
- **NLP**: transformers

## Setup Instructions

### Backend
1. Create virtual env for backend
    ```bash
    python -m venv env

2. Activate created virtual env for backend
- For windows
    ```bash
    . \env\Scripts\activate

- For ubuntu
    source env/bin/activate

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Run backend
    - To run this you need to stay in main project folder not in backend folder
    ```bash
    uvicorn backend.main:app --reload

5. Run frontend
    - To run this stay in frontend folder
    ```bash
    npm start
