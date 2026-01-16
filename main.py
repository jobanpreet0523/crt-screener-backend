from fastapi import FastAPI

app = FastAPI(title="CRT Screener Backend")

@app.get("/")
def root():
    return {"status": "CRT backend running"}

@app.get("/health")
def health():
    return {"ok": True}
