from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from sqlalchemy.orm import Session
from .database import SessionLocal, PDFDocument, init_db
from .services import extract_text_from_pdf, answer_question

app = FastAPI()

# Allow CORS from localhost:3000 (where your React app is running)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow React app's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    # Ensure the 'uploaded_pdfs' directory exists
    upload_dir = "./uploaded_pdfs"
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, file.filename)
    
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    text_content = extract_text_from_pdf(file_path)

    db = SessionLocal()
    pdf_document = PDFDocument(filename=file.filename, content=text_content)
    db.add(pdf_document)
    db.commit()
    db.close()

    return {"message": "File uploaded successfully", "filename": file.filename}

@app.post("/ask/")  # Assuming you also need CORS for the ask endpoint
async def ask_question(filename: str = Form(...), question: str = Form(...)):
    db = SessionLocal()
    
    # Ensure that the filename includes ".pdf"
    if not filename.endswith(".pdf"):
        filename += ".pdf"

    pdf_doc = db.query(PDFDocument).filter(PDFDocument.filename == filename).first()
    db.close()
    if not pdf_doc:
        raise HTTPException(status_code=404, detail="PDF not found")

    document_content = pdf_doc.content

    answer = answer_question(document_content, question)
    return {"answer": answer}
