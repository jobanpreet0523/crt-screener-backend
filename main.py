print("FASTAPI APP STARTING...")

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
from database import Base, engine, SessionLocal
from models import User, Scan
from auth import hash_pw, verify_pw, create_token, decode_token

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------- AUTH --------

@app.post("/signup")
def signup(u: dict, db=Depends(get_db)):
    if db.query(User).filter_by(username=u["username"]).first():
        raise HTTPException(400, "User exists")
    db.add(User(username=u["username"], password=hash_pw(u["password"])))
    db.commit()
    return {"msg": "ok"}

@app.post("/login")
def login(u: dict, db=Depends(get_db)):
    user = db.query(User).filter_by(username=u["username"]).first()
    if not user or not verify_pw(u["password"], user.password):
        raise HTTPException(401, "Invalid credentials")
    return {"token": create_token(user.username)}

# -------- CRT LOGIC --------

def crt(df):
    p, c = df.iloc[-2], df.iloc[-1]
    eq = (p.High + p.Low) / 2

    if c.Low < p.Low and p.Low < c.Close < p.High and c.Close < eq:
        return "BUY CRT"

    if c.High > p.High and p.Low < c.Close < p.High and c.Close > eq:
        return "SELL CRT"

@app.get("/scan")
def scan(tf="daily", min_price=10, min_volume=1_000_000):
    interval = {"daily": "1d", "weekly": "1wk", "monthly": "1mo"}[tf]
    tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "META"]

    results = []

    for t in tickers:
        df = yf.download(t, period="6mo", interval=interval, progress=False)
        if len(df) < 10:
            continue

        signal = crt(df)
        if signal and df.Close.iloc[-1] >= min_price and df.Volume.iloc[-1] >= min_volume:
            results.append({"symbol": t, "signal": signal})

    return results
