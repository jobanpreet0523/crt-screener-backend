from fastapi import FastAPI
from batch_scan import run_nse200_scan

app = FastAPI(title="CRT Screener Backend")

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/scan/nse200")
def scan_nse200():
    results = run_nse200_scan()
    return {
        "count": len(results),
        "results": results
    }
