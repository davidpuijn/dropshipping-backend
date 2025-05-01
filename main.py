import os
import uuid
import httpx
import openai
from datetime import datetime
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
API_KEY = os.getenv("LOCAL_API_KEY", "MY_SECRET_API_KEY")

headers = {
    "apikey": SUPABASE_API_KEY,
    "Authorization": f"Bearer {SUPABASE_API_KEY}",
    "Content-Type": "application/json"
}

learned_keywords = set(["aliexpress", "2-4 weeks", "shipping from china", "warehouse delay"])

class SiteCheckRequest(BaseModel):
    url: str
    text: str

class ReportRequest(BaseModel):
    url: str
    status: str
    text: str = ""

def authorize(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/report")
async def report_site(data: ReportRequest, x_api_key: str = Header(None)):
    authorize(x_api_key)

    if data.status == "dropshipping" and data.text:
        for word in data.text.lower().split():
            if any(k in word for k in ["ali", "china", "shipping", "delivery", "weeks"]):
                print(f"Nieuw trefwoord geleerd: {{word.strip(',.!?')}}")
            learned_keywords.add(word.strip(",.!?"))

    payload = {
        "id": str(uuid.uuid4()),
        "url": data.url,
        "status": data.status,
        "reported_at": datetime.utcnow().isoformat()
    }

    async with httpx.AsyncClient() as client:
        await client.post(f"{SUPABASE_URL}/rest/v1/reports", headers=headers, json=payload)

    return {"message": "Reported to Supabase and learned keywords", "data": payload, "keywords": list(learned_keywords)}

@app.get("/reports")
async def get_reports():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{SUPABASE_URL}/rest/v1/reports?select=url,status,reported_at", headers=headers)
        return r.json()

@app.post("/analyze")
async def analyze_site(data: SiteCheckRequest, x_api_key: str = Header(None)):
    authorize(x_api_key)

    heuristics_score = score_by_keywords(data.text)
    reputation_score = await score_by_web_reputation(data.url)
    final_score = heuristics_score + reputation_score

    if final_score >= 2:
        print(f"AI detecteerde: {{data.url}} met status: \"dropshipping\"")
        await report_site(ReportRequest(url=data.url, status="dropshipping", text=data.text), x_api_key)
        return {"status": "dropshipping", "score": final_score}
    elif final_score <= -1:
        print(f"AI detecteerde: {{data.url}} met status: \"dropshipping\"")
        await report_site(ReportRequest(url=data.url, status="safe", text=data.text), x_api_key)
        print(f"AI detecteerde: {data.url} met status: \"safe\"")
        return {"status": "safe", "score": final_score}
    else:
        print(f"AI detecteerde: {data.url} met status: \"unknown\"")
        return {"status": "unknown", "score": final_score}

def score_by_keywords(text: str) -> int:
    score = 0
    for word in learned_keywords:
        if word in text.lower():
            score += 1
    return score

async def score_by_web_reputation(domain: str) -> int:
    trustpilot_url = f"https://www.trustpilot.com/review/{domain}"
    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(trustpilot_url, timeout=10)
            content = r.text.lower()
            if any(bad in content for bad in ['scam', 'fake', 'bad service']):
                return 1
            elif any(good in content for good in ['legit', 'great service']):
                return -1
        except:
            pass
    return 0
