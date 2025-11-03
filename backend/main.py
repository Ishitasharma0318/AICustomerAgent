"""
FastAPI application entry point
Multi-agent customer service AI for AWS Lambda and API Gateway
"""

import os
import logging
import time
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from dotenv import load_dotenv

from routers import chat_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Advanced Customer Service AI",
    description="Multi-agent system for AWS Lambda and API Gateway support",
    version="1.0.0",
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


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and responses"""
    request_id = request.headers.get("X-Request-ID", "unknown")
    start_time = time.time()
    
    # Log request
    logger.info(f"[{request_id}] {request.method} {request.url.path}")
    
    try:
        # Process request
        response = await call_next(request)
        
        # Log response
        duration = time.time() - start_time
        logger.info(
            f"[{request_id}] Completed {request.method} {request.url.path} "
            f"- Status: {response.status_code} - Duration: {duration:.3f}s"
        )
        
        # Add custom headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(duration)
        
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            f"[{request_id}] Failed {request.method} {request.url.path} "
            f"- Duration: {duration:.3f}s - Error: {str(e)}",
            exc_info=True
        )
        raise


# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP error: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "details": exc.errors(),
            "path": str(request.url.path),
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "path": str(request.url.path),
        },
    )


# Include routers
app.include_router(chat_router, prefix="/api", tags=["chat"])


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("=" * 70)
    logger.info("🚀 Advanced Customer Service AI - Multi-Agent System")
    logger.info("=" * 70)
    logger.info("Version: 1.0.0")
    logger.info("Environment: " + os.getenv("ENVIRONMENT", "development"))
    logger.info("=" * 70)


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("=" * 70)
    logger.info("🛑 Shutting down Advanced Customer Service AI")
    logger.info("=" * 70)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "status": "running",
        "message": "Advanced Customer Service AI - Multi-Agent System",
        "version": "1.0.0",
        "docs_url": "/docs",
        "endpoints": {
            "chat": "/api/chat",
            "chat_stream": "/api/chat/stream",
            "health": "/health",
            "metrics": "/metrics",
        },
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": time.time(),
    }


@app.get("/metrics")
async def metrics():
    """Simple metrics endpoint"""
    # In production, you'd integrate with Prometheus or similar
    return {
        "status": "operational",
        "version": "1.0.0",
        # Add more metrics as needed
    }


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info",
    )

