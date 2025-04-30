from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import re
import openai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS-middleware toestaan
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Of specifieker: ["chrome-extension://<extensie-id>"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === CONFIG ===
openai.api_key = "YOUR_OPENAI_API_KEY"  # <- Vul dit aan

class SiteCheckRequest(BaseModel):
    url: str
    text: str

@app.post("/analyze")
async def analyze_site(data: SiteCheckRequest):
    heuristics_score = score_by_keywords(data.text)
    reputation_score = await score_by_web_reputation(data.url)
    final_score = heuristics_score + reputation_score

    if final_score >= 2:
        return {"status": "dropshipping", "score": final_score}
    elif final_score <= -1:
        return {"status": "safe", "score": final_score}
    else:
        return {"status": "unknown", "score": final_score}

def score_by_keywords(text: str) -> int:
    keywords = ['aliexpress', '2-4 weeks', 'shipping from china', 'warehouse delay']
    return sum([1 for word in keywords if word in text.lower()])

async def score_by_web_reputation(domain: str) -> int:
    query = f"{domain} reviews site:trustpilot.com OR site:reddit.com"
    async with httpx.AsyncClient() as client:
        google_search_url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = await client.get(google_search_url, headers=headers)

    if "trustpilot" in response.text.lower() or "scam" in response.text.lower():
        return 1
    elif "legit" in response.text.lower():
        return -1
    else:
        return 0
        
