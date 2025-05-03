from fastapi import APIRouter, Request
from ai_utils import analyze_text
import json

router = APIRouter()

with open("keywords/default_keywords.json") as f:
    keywords = json.load(f)

@router.post("/analyze2")
async def analyze(request: Request):
    data = await request.json()
    text = data.get("text", "").lower()
    url = data.get("url", "")
    result, score = analyze_text(text, keywords)
    return {"result": result, "score": score, "url": url}
