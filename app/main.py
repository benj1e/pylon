from fastapi import FastAPI, Request
from app.api.router import api_router
import time

app = FastAPI(title="Pylon")


@app.middleware("http")
async def add_timer_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(api_router)


@app.get("/")
async def root() -> dict[str, str]:
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to Pylon"}
