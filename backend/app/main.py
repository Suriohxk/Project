"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

from app.routes.chat import router as chat_router

app = FastAPI(
    title="Waste Classification & Smart Disposal Assistant",
    description="AI-powered waste segregation guidance aligned with SDG 12 — for Indian households.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)


@app.get("/")
async def root():
    return {
        "message": "♻️ Waste Classification Assistant API is running.",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
