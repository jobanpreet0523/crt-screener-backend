from fastapi import FastAPI, Query

app = FastAPI(title="CRT Screener Backend")

@app.get("/")
def health():
    return {"status": "OK", "service": "CRT Backend"}

@app.get("/scan")
def scan(tf: str = Query(default="daily")):
    return {
        "timeframe": tf,
        "message": "Scan endpoint live",
        "results": []
    }
