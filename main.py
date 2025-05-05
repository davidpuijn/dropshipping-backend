from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import openai

# Laad API keys en Supabase config
load_dotenv()
API_KEY = os.getenv("LOCAL_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
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
    keywords_data = supabase.table("keywords").select("keywords").execute()
    keywords = [item["keywords"] for item in keywords_data.data] if keywords_data.data else []

    score = sum(1 for word in keywords if word in request.text.lower())
    status = "dropshipping" if score >= 2 else "safe"
    
    return {"status": status, "score": score}
@app.post("/report")
async def report(request: Request):
    data = await request.json()
    print("Ontvangen data:", data)

    try:
        response = supabase.table("reports").insert(data).execute()
        print("Supabase response:", response)
        return {"message": "Report stored"}
    except Exception as e:
        print("Fout bij insert:", e)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/debug")
async def debug_report(request: Request):
    """Debug endpoint voor handmatige testmeldingen"""
    body = await request.json()
    supabase.table("reports").insert({
        "url": body["url"],
        "text": body["text"],
        "status": body.get("reason", "debug"),
        "ai_created": False
    }).execute()
    return {"message": "Debugmelding opgeslagen"}

@app.post("/bulk_keywords")
async def bulk_keywords(request: Request):
    """Voeg meerdere trefwoorden tegelijk toe"""
    try:
        items = await request.json()
        response = supabase.table("keywords").insert(items).execute()
        print("Bulk insert response:", response)
        return {"message": "Bulk insert gelukt", "items": len(items)}
    except Exception as e:
        print("Fout bij bulk insert:", e)
        raise HTTPException(status_code=500, detail=str(e))



