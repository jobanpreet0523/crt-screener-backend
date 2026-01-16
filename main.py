from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from crt_logic import run_crt_scan   # IMPORTANT

app = FastAPI()

# ✅ CORS (VERY IMPORTANT for Vercel frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later you can restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "CRT Backend Running"}

# ✅ THIS IS THE MISSING / BROKEN PART
@app.get("/scan")
def scan(tf: str = "daily"):
    """
    Example:
    /scan?tf=daily
    /scan?tf=weekly
    """
    results = run_crt_scan(tf)
    return results
