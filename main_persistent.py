from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
import httpx
import re
import openai
import json
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = "{DEDC9729/12BZPM@}"
API_KEY = "{DEDC9729/12BZPM@}"
STORAGE_FILE = "reported_sites.json"

# Laad bestaande data
if os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "r") as f:
        reported_sites = json.load(f)
else:
    reported_sites = {}

class SiteCheckRequest(BaseModel):
    url: str
    text: str

class ReportRequest(BaseModel):
    url: str
    status: str

def authorize(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

def save_reports():
    with open(STORAGE_FILE, "w") as f:
        json.dump(reported_sites, f)

@app.post("/analyze")
async def analyze_site(data: SiteCheckRequest, x_api_key: str = Header(None)):
    authorize(x_api_key)

    if data.url in reported_sites:
        return {"status": reported_sites[data.url], "source": "user-report"}

    heuristics_score = score_by_keywords(data.text)
    reputation_score = await score_by_web_reputation(data.url)
    final_score = heuristics_score + reputation_score

    if final_score >= 2:
        reported_sites[data.url] = "dropshipping"
        save_reports()
        return {"status": "dropshipping", "score": final_score}
    elif final_score <= -1:
        reported_sites[data.url] = "safe"
        save_reports()
        return {"status": "safe", "score": final_score}
    else:
        return {"status": "unknown", "score": final_score}

@app.post("/report")
async def report_site(data: ReportRequest, x_api_key: str = Header(None)):
    authorize(x_api_key)
    reported_sites[data.url] = data.status
    save_reports()
    return {"message": "Report opgeslagen", "url": data.url, "status": data.status}

@app.get("/reports")
async def get_reports():
    return reported_sites

def score_by_keywords(text: str) -> int:
    keywords = ['aliexpress', '2-4 weeks', 'shipping from china', 'warehouse delay']
    return sum([1 for word in keywords if word in text.lower()])

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
