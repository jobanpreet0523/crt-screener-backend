from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

from database import Base, engine, SessionLocal
from models import User, Scan
from auth import hash_pw, verify_pw, create_token, decode_token

print("FASTAPI APP STARTING...")

# Create DB tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app FIRST
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root health check
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "CRT Screener Backend is running",
        "docs": "/docs"
    }

