from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="CRT Screener Backend",
    description="FastAPI backend for CRT trading screener",
    version="1.0.0",
)

# CORS (safe default – frontend friendly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check (VERY IMPORTANT for Railway)
@app.get("/")
def health_check():
    return {"status": "alive", "service": "crt-screener-backend"}

# Example test endpoint
@app.get("/ping")
def ping():
    return {"message": "pong"}

# --- future CRT endpoints go below ---
# @app.get("/scan")
# def scan():
#     return {"result": "scanner coming soon"}
