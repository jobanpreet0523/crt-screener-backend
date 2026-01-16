from fastapi import FastAPI, Query
from scanner import run_crt_scan

app = FastAPI(
    title="CRT Screener Backend",
    version="1.0.0"
)


@app.get("/")
def health_check():
    return {"status": "CRT Backend Running"}


@app.get("/scan")
def scan(tf: str = Query(default="daily")):
    return run_crt_scan(tf)
