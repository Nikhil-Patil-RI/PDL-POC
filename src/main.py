"""
PDL-POC Main Application Entry Point

This is a Proof of Concept for People Data Labs integration
for prospect preview and generation.
"""

import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Load environment variables
load_dotenv()

# Import routers
from src.api.companies import router as companies_router
from src.api.prospects import router as prospects_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("🚀 PDL-POC API Starting...")
    yield
    # Shutdown
    print("👋 PDL-POC API Shutting down...")


app = FastAPI(
    title="PDL-POC API",
    description="Proof of Concept for People Data Labs integration",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(prospects_router, prefix="/api/v1", tags=["prospects"])
app.include_router(companies_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "pdl-poc"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "PDL-POC API",
        "version": "0.1.0",
        "docs": "/docs",
    }

