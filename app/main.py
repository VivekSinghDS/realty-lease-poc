from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import asyncio
import os
import json 

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse

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
        "prefix": "/misc",
        "tags": ["other"],
    },
    {
        "router": lease_abstraction.router,
        "prefix": "/lease",
        "tags": ['lease']
    }
    # Commented out until content_entries is implemented
    # {"router": content_entries.router, "prefix": "/entries", "tags": ["entries"]},
]


for route in routers:
    app.include_router(route["router"], prefix=route["prefix"], tags=route["tags"])
    
app.add_middleware(CORSMiddleware, **CORS_CONFIG)
@app.get("/")
async def root():
    return {"message": "Stealth!"}


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "environment": os.environ.get("ENVIRONMENT", "unknown"),
        "version": "1.0.0"
    }
    
@app.post('/sample-stream')
async def sample_stream():
    with open("/Users/vivek.singh/realty-poc/utils/references/reference_updation.json", "r") as file:
        json_data = json.load(file)
        
    json_str = json.dumps(json_data, indent=2)

    async def char_stream():
        for character in json_str:
            yield character
            await asyncio.sleep(0.01)  # optional delay to simulate real streaming

    return StreamingResponse(char_stream(), media_type="application/json")
