from fastapi import FastAPI
from .db import supabase

app = FastAPI(
    title="CV Matcher API",
    description="Backend service for CV scoring & ranking",
    version="0.1.0"
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "FastAPI backend running"}

@app.get("/jobs")
def get_jobs():
    response = supabase.table("job_descriptions").select("*").execute()
    return {"jobs": response.data}
