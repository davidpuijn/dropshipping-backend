from fastapi import FastAPI
from routes import analyze, report

app = FastAPI()

app.include_router(analyze.router)
app.include_router(report.router)

@app.get("/")
def read_root():
    return {"message": "Dropshipping backend live!"}
