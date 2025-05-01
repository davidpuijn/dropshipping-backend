from fastapi import FastAPI, Request, Header
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os, re, httpx
from datetime import datetime

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOCAL_API_KEY = os.getenv("LOCAL_API_KEY")

learned_keywords = {"shipping", "aliexpress", "china", "2-4 weeks", "warehouse", "supplier", "reseller", "delivered from abroad"}

class SiteData(BaseModel):
    url: str
    text: str

async def report_site(url: str, status: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{SUPABASE_URL}/rest/v1/reports",
            headers={
                "apikey": SUPABASE_API_KEY,
                "Authorization": f"Bearer {SUPABASE_API_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            },
            json={"url": url, "status": status, "reported_at": datetime.utcnow().isoformat()}
        )

@app.post("/analyze")
async def analyze(data: SiteData, x_api_key: str = Header(None)):
    if x_api_key != LOCAL_API_KEY:
        return {"error": "Unauthorized"}

    score = 0
    found = []

    for word in learned_keywords:
        if word in data.text.lower():
            score += 1
            found.append(word)

    final_score = score
    if final_score >= 3:
        print(f"AI detecteerde: {data.url} met status: \"dropshipping\"")
        await report_site(data.url, "dropshipping")
        return {"status": "dropshipping", "score": final_score}
    elif final_score == 2:
        print(f"AI detecteerde: {data.url} met status: \"unknown\"")
        return {"status": "unknown", "score": final_score}
    else:
        print(f"AI detecteerde: {data.url} met status: \"safe\"")
        return {"status": "safe", "score": final_score}

@app.post("/report")
async def manual_report(data: SiteData, x_api_key: str = Header(None)):
    if x_api_key != LOCAL_API_KEY:
        return {"error": "Unauthorized"}

    # Leer nieuwe woorden
    words = re.findall(r'\b\w+\b', data.text.lower())
    for word in words:
        if word not in learned_keywords and len(word) > 3:
            print(f"Nieuw trefwoord geleerd: {word}")
            learned_keywords.add(word)

    await report_site(data.url, data.text)
    return {"message": "Gemeld en opgeslagen."}

@app.get("/reports")
async def get_reports(x_api_key: str = Header(None)):
    if x_api_key != LOCAL_API_KEY:
        return {"error": "Unauthorized"}

    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{SUPABASE_URL}/rest/v1/reports?select=*",
            headers={
                "apikey": SUPABASE_API_KEY,
                "Authorization": f"Bearer {SUPABASE_API_KEY}"
            }
        )
        return res.json()
