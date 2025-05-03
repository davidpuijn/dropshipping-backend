from fastapi import APIRouter, Request
from supabase import supabase

router = APIRouter()

@router.post("/report2")
async def report(request: Request):
    data = await request.json()
    supabase.table("reports").insert(data).execute()
    return {"status": "saved"}
