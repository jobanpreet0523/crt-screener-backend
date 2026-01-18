from fastapi import FastAPI
from batch_scan import run_batch_scan

app = FastAPI()

@app.get("/")
def health():
    return {"status": "alive"}

@app.get("/api/crt-scan")
def crt_scan():
    return {
        "status": "ok",
        "results": run_batch_scan()
    }
