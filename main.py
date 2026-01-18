from fastapi import FastAPI
from storage import load_results

app = FastAPI()


@app.get("/")
def health():
    return {"status": "CRT backend live"}


@app.get("/scan/nse200")
def get_scan_results():
    return load_results()["results"]
