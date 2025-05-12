from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import openai

# ✅ Laad .env variabelen
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOCAL_API_KEY = os.getenv("LOCAL_API_KEY")

# ✅ Init Supabase & OpenAI
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
openai.api_key = OPENAI_API_KEY

# ✅ Init FastAPI
app = FastAPI()

# ✅ CORS instellingen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request-modellen
class AnalyzeRequest(BaseModel):
    url: str
    text: str
    reason: str = ""

class ReportRequest(BaseModel):
    url: str
    text: str
    reason: str

# ✅ /analyze endpoint — veilig, alleen tekst-gebaseerd
@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    try:
        keywords_data = supabase.table("keywords").select("term").execute()
        keywords = [item["term"].lower() for item in keywords_data.data] if keywords_data.data else []

        text = request.text.lower()
        score = sum(1 for word in keywords if word in text)

        status = "dropshipping" if score >= 2 else "twijfelachtig" if score == 1 else "safe"

        supabase.table("reports").insert({
            "url": request.url,
            "text": request.text,
            "status": status,
            "reason": "auto-analysis",
            "ai_created": True
        }).execute()

        return {"status": status, "score": score}

    except Exception as e:
        print("Fout tijdens analyse:", e)
        raise HTTPException(status_code=500, detail=str(e))

# ✅ /report — handmatige meldingen
@app.post("/report")
async def report(request: Request):
    try:
        data = await request.json()
        supabase.table("reports").insert(data).execute()
        return {"message": "Report opgeslagen"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ /bulk_keywords — meerdere trefwoorden tegelijk toevoegen
@app.post("/bulk_keywords")
async def bulk_keywords(request: Request):
    try:
        items = await request.json()
        supabase.table("keywords").insert(items).execute()
        return {"message": "Bulk insert gelukt", "items": len(items)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
