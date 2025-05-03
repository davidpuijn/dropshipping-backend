from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    text = data.get("text", "")
    url = data.get("url", "")
    
    keywords = ["verzending 2-3 weken", "rechtstreeks uit magazijn", "dropship", "lage prijs", "AliExpress"]
    if any(k in text.lower() for k in keywords):
        return {"result": "dropshipping", "source": "local-keywords"}
    
    prompt = f"Beoordeel of de volgende website dropshipping is: {text[:3000]}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        ai_result = response.choices[0].message.content.lower()
        if "dropshipping" in ai_result:
            return {"result": "dropshipping", "source": "ai"}
    except Exception as e:
        return {"result": "safe", "error": str(e)}

    return {"result": "safe", "source": "ai"}