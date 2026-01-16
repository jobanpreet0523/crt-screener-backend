from fastapi import FastAPI

app = FastAPI(title="CRT Screener Backend")

@app.api_route("/", methods=["GET", "HEAD"])
def root():
    return {"status": "CRT backend running"}
