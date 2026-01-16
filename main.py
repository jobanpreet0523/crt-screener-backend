from fastapi import FastAPI, Query

app = FastAPI(title="CRT Screener Backend")

@app.get("/")
def root():
    return {"status": "CRT Backend Running"}

@app.get("/scan")
def scan(tf: str = Query(default="daily")):
    return {
        "timeframe": tf,
        "message": "Scan endpoint live",
        "results": []
    }
