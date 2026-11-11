
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def home(request: Request):
    return {
        "message": "Request received",
        "server": request.url.port
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
