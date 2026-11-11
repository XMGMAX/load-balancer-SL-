
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx
import asyncio

app = FastAPI()

servers = [
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",
    "http://127.0.0.1:8003"
]

current_server = 0
lock = asyncio.Lock()


@app.get("/")
async def load_balance():
    global current_server

    async with lock:
        server = servers[current_server]
        current_server = (current_server + 1) % len(servers)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(server)

            return JSONResponse(
                content=response.json(),
                status_code=response.status_code
            )

        except httpx.RequestError:
            return JSONResponse(
                content={"error": "Backend unavailable"},
                status_code=503
            )
