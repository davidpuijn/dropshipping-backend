from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import openai

# Laad .env variabelen
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Supabase en OpenAI setup
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
openai.api_key = OPENAI_API_KEY

app = FastAPI()

# CORS-configuratie
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request-modellen
class AnalyzeRequest(BaseModel):
    url: str
    text: str

class ReportRequest(BaseModel):
    url: str
    text: str
    reason: str

class TrainRequest(BaseModel):
    url: str
    text: str

# AI-analyse endpoint
@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        keywords_data = supabase.table("keywords").select("term").execute()
        keywords = [item["term"] for item in keywords_data.data] if keywords_data.data else []
        score = sum(1 for word in keywords if word in request.text.lower())
        status = "dropshipping" if score >= 2 else "safe"
        return {"status": status, "score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Melden van verdachte sites
@app.post("/report")
async def report(request: Request):
    data = await request.json()
    try:
        supabase.table("reports").insert(data).execute()
        return {"message": "Report opgeslagen"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Debug/test endpoint
@app.post("/debug")
async def debug_report(request: Request):
    body = await request.json()
    try:
        supabase.table("reports").insert({
            "url": body["url"],
            "text": body["text"],
            "status": body.get("reason", "debug"),
            "ai_created": False
        }).execute()
        return {"message": "Debugmelding opgeslagen"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Bulk keywords upload
@app.post("/bulk_keywords")
async def bulk_keywords(request: Request):
    try:
        items = await request.json()
        for item in items:
            item.setdefault("source_url", "manual")
        supabase.table("keywords").insert(items).execute()
        return {"message": "Bulk insert gelukt", "items": len(items)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Zelflerende keyword training
@app.post("/train")
async def train_keywords(request: TrainRequest):
    try:
        text = request.text.lower()
        url = request.url
        existing = supabase.table("keywords").select("term").execute()
        known_terms = {item["term"] for item in existing.data} if existing.data else set()
        words = set(text.replace(",", "").replace(".", "").split())
        new_terms = [{"term": w, "source_url": url} for w in words if w not in known_terms and len(w) > 2]

        if new_terms:
            supabase.table("keywords").insert(new_terms).execute()

        return {"message": f"{len(new_terms)} nieuwe trefwoorden toegevoegd", "terms": new_terms}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

