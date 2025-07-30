# app/api/router.py
from fastapi import APIRouter
from .endpoints import process

api_router = APIRouter()
api_router.include_router(process.router, tags=["process"])
