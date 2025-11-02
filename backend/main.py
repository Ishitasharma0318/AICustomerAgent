"""
FastAPI application entry point
Multi-agent customer service AI for AWS Lambda and API Gateway
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import chat_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Advanced Customer Service AI",
    description="Multi-agent system for AWS Lambda and API Gateway support",
    version="0.1.0",
)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api", tags=["chat"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "message": "Advanced Customer Service AI - Multi-Agent System",
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
    )

