from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import openai

# Laad API keys en Supabase config
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
openai.api_key = OPENAI_API_KEY

app = FastAPI()

# CORS toestaan
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Toestaan vanuit alle domeinen (voor extensie)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request modellen
class AnalyzeRequest(BaseModel):
    url: str
    text: str

class ReportRequest(BaseModel):
    url: str
    text: str
    reason: str = "Handmatig gemeld"

# AI-analyse route
@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    keywords_data = supabase.table("keywords").select("term").execute()
    keywords = [item["term"] for item in keywords_data.data] if keywords_data.data else []
    score = sum(1 for word in keywords if word in request.text.lower())
    status = "dropshipping" if score >= 2 else "safe"
    return {"status": status, "score": score}

# Melding opslaan
@app.post("/report")
async def report(request: ReportRequest):
    data = {
        "url": request.url,
        "text": request.text,
        "reason": request.reason,
        "ai_trained": False,
        "editable": True,
        "log": "Aangemeld via extensie"
    }
    supabase.table("reports").insert(data).execute()
    return {"message": "Melding ontvangen en opgeslagen"}

