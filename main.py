from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CRT Screener Backend")

# --------------------
# CORS (SAFE)
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Health Check (MANDATORY)
# --------------------
@app.get("/")
def root():
    return {"status": "OK", "service": "CRT Screener Backend"}

# --------------------
# Scan Endpoint (SAFE IMPORT)
# --------------------
@app.get("/scan")
def scan(tf: str = "daily"):
    try:
        from scanner import run_scan
        return run_scan(tf)
    except Exception as e:
        return {
            "error": "Scanner failed",
            "details": str(e)
        }
