from fastapi import FastAPI
from sessions import get_current_session

app = FastAPI(title="CRT Screener Backend")

@app.get("/")
def root():
    return {"status": "CRT backend running"}

@app.get("/session")
def session():
    return {"session": get_current_session()}
