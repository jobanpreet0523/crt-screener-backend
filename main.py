from fastapi import FastAPI

app = FastAPI()

# HEALTH CHECK
@app.get("/")
def root():
    return {"status": "ok", "message": "CRT Screener Backend Running"}

# REGISTER
@app.post("/register")
def register(user: dict):
    return {
        "msg": "User registered successfully",
        "username": user.get("username")
    }

# LOGIN
@app.post("/login")
def login(user: dict):
    return {
        "msg": "Login successful",
        "username": user.get("username"),
        "token": "dummy-token"
    }

# SCAN
@app.get("/scan")
def scan(tf: str = "daily"):
    return {
        "timeframe": tf,
        "results": [
            {"symbol": "AAPL", "signal": "BUY CRT"},
            {"symbol": "MSFT", "signal": "SELL CRT"}
        ]
    }
