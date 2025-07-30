from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(title="Pylon")

app.include_router(api_router)

@app.get("/")
async def root() -> dict[str, str]:
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to Pylon"}
