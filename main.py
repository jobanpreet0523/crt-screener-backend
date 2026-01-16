from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI(title="CRT Screener Backend")

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "CRT backend running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/favicon.ico")
def favicon():
    return Response(status_code=204)
