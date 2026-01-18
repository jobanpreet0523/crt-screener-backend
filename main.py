from fastapi import FastAPI
from batch_scan import run_nse200_scan

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/scan/nse200")
def scan_nse_200():
    return {
        "count": len(run_nse200_scan()),
        "results": run_nse200_scan()
    }
