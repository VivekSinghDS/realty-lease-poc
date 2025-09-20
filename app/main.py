from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import asyncio
import os


from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers import lease_abstraction, minimum_lease_terms
from utils.constants import CORS_CONFIG
  
app = FastAPI()

@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        # Set a reasonable timeout for all requests
        response = await asyncio.wait_for(call_next(request), timeout=300.0)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except asyncio.TimeoutError:
        return {"error": "Request timeout", "detail": "Request took too long to process"}

routers = [
    {
        "router": minimum_lease_terms.router,
        "prefix": "/lease-summary",
        "tags": ["lease-summary"],
    },
    {
        "router": lease_abstraction.router,
        "prefix": "/lease-abstract",
        "tags": ['lease-abstract']
    }
    # Commented out until content_entries is implemented
    # {"router": content_entries.router, "prefix": "/entries", "tags": ["entries"]},
]

app.add_middleware(CORSMiddleware, **CORS_CONFIG)

for route in routers:
    app.include_router(route["router"], prefix=route["prefix"], tags=route["tags"])
    
@app.get("/")
async def root():
    return {"message": "ask-ai main page!"}


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "environment": os.environ.get("ENVIRONMENT", "unknown"),
        "version": "1.0.0"
    }