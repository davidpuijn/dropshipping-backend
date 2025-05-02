from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import openai
import requests
from supabase import create_client

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOCAL_API_KEY = os.getenv("LOCAL_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)
openai.api_key = OPENAI_API_KEY

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    url = data.get("url", "")
    text = data.get("text", "")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Detecteer of dit dropshipping is."},
            {"role": "user", "content": f"URL: {url}

{text}"}
        ]
    )

    result_text = response.choices[0].message.content.lower()
    result = "dropshipping" if "dropshipping" in result_text else "safe"

    return {"result": result}

@app.post("/report")
async def report(request: Request):
    data = await request.json()
    url = data.get("url")
    text = data.get("text")

    if url and text:
        supabase.table("reports").insert({"url": url, "text": text}).execute()
        return {"status": "saved"}
    return {"error": "invalid input"}
