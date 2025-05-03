from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import openai

# Laad API keys en Supabase config
load_dotenv()
API_KEY = os.getenv("LOCAL_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)
openai.api_key = OPENAI_API_KEY

app = FastAPI()

# CORS instellingen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    url: str
    text: str

class ReportRequest(BaseModel):
    url: str
    text: str
    reason: str

@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    """Voer eenvoudige AI-analyse uit"""
    keywords_data = supabase.table("keywords").select("term").execute()
    keywords = [item["term"] for item in keywords_data.data] if keywords_data.data else []

    score = sum(1 for word in keywords if word in request.text.lower())
    status = "dropshipping" if score >= 2 else "safe"
    
    return {"status": status, "score": score}

@app.post("/report")
async def report(request: ReportRequest):
    """Sla handmatige meldingen op in Supabase"""
    data = {
        "url": request.url,
        "text": request.text,
        "reason": request.reason,
        "ai_trained": False,
        "editable": True,
        "log": f"Aangemeld door extensie-gebruiker"
    }
    supabase.table("reports").insert(data).execute()
    return {"message": "Website is gemeld voor onderzoek"}

