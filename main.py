from fastapi import FastAPI
from batch_scan import run_batch_scan

app = FastAPI()

@app.get("/")
def health():
    return {"status": "alive"}

@app.get("/api/nse-batch-scan")
def nse_batch_scan():
    results = run_batch_scan()

    return {
        "status": "ok",
        "count": len(results),
        "results": results
    }
