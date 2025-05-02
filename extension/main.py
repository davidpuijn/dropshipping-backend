
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Optional
import datetime

load_dotenv()

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# Models
class AnalyzeRequest(BaseModel):
    url: str
    text: str

class ReportRequest(BaseModel):
    url: str
    text: Optional[str] = ""

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    keywords = ["shipping from china", "delivered in 2-4 weeks", "aliexpress", "warehouse overseas"]
    score = sum(1 for word in keywords if word in request.text.lower())

    # Supabase logging (optioneel)
    supabase.table("keywords").insert({ "source_url": request.url, "matched_score": score, "timestamp": datetime.datetime.utcnow().isoformat() }).execute()

    status = "dropshipping" if score >= 2 else "safe"
    return { "status": status, "score": score }

@app.post("/report")
async def report(req: ReportRequest):
    supabase.table("reports").insert({
        "url": req.url,
        "text": req.text,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }).execute()
    return { "message": "Report saved", "url": req.url }
