from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CRT Screener Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "LIVE",
        "message": "CRT Screener Backend is running"
    }

@app.get("/health")
def health():
    return {"ok": True}
