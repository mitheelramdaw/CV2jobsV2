from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from PyPDF2 import PdfReader
import spacy
import re
from .db import supabase

app = FastAPI(
    title="CV Matcher API",
    description="Backend service for CV scoring & ranking",
    version="1.0.0"
)

# load spaCy model once
nlp = spacy.load("en_core_web_md")

def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    return " ".join(tokens)

def calculate_similarity(cv_text: str, job_text: str) -> float:
    cv_doc = nlp(preprocess(cv_text))
    job_doc = nlp(preprocess(job_text))
    return cv_doc.similarity(job_doc) * 100

@app.get("/")
def health_check():
    return {"status": "ok", "message": "FastAPI backend running"}

@app.get("/jobs")
def get_jobs():
    try:
        response = supabase.table("job_descriptions").select("*").execute()
        return {"jobs": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload_cv")
async def upload_cv(job_id: str = Form(...), file: UploadFile = File(...)):
    try:
        # Extract CV text from PDF
        reader = PdfReader(file.file)
        cv_text = ""
        for page in reader.pages:
            cv_text += page.extract_text() or ""

        # Fetch job description
        job = supabase.table("job_descriptions").select("*").eq("id", job_id).execute()
        if not job.data:
            raise HTTPException(status_code=404, detail="Job not found")

        job_desc = job.data[0]["description"]

        # Calculate similarity
        score = calculate_similarity(cv_text, job_desc)

        return {"status": "ok", "score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
