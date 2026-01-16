from fastapi import FastAPI
from scanner import run_crt_scan

app = FastAPI()

@app.get("/")
def root():
    return {"status": "CRT Backend Running"}

@app.get("/scan")
def scan(tf: str = "daily"):
    return run_crt_scan(tf)
