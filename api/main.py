#!/usr/bin/env python3
"""
Pharma Intelligence API - Main Application
FastAPI backend for drug analysis platform
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import time

from routes import router
from models import ErrorResponse

# ============================================================================
# APPLICATION SETUP
# ============================================================================

app = FastAPI(
    title="Pharma Intelligence API",
    description="""
    **Drug Analysis Platform for Pharmaceutical Targeting**
    
    This API provides comprehensive prescribing pattern analysis for pharmaceutical products.
    
    ## Features
    
    * 🎯 **Drug Analysis** - Identify top prescriber opportunities
    * 🔍 **Drug Search** - Find drug codes by name
    * 📊 **Market Intelligence** - Segmentation and recommendations
    * 🌍 **Multi-Country** - Pluggable data sources (UK available, US/EU coming)
    
    ## Quick Start
    
    1. Search for your drug: `POST /drugs/search`
    2. Run analysis: `POST /analyze`
    3. Get actionable insights
    
    ## Rate Limits
    
    * Free tier: 10 requests/hour
    * Paid tier: Unlimited
    
    ## Authentication
    
    Coming soon - currently open access for testing
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "General", "description": "Health checks and info"},
        {"name": "Reference", "description": "Reference data (countries, etc.)"},
        {"name": "Drugs", "description": "Drug search and lookup"},
        {"name": "Analysis", "description": "Core analysis endpoints"}
    ]
)

# ============================================================================
# MIDDLEWARE
# ============================================================================

# CORS - Allow all origins for now (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests (basic version)"""
    print(f"[{datetime.now().isoformat()}] {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"  → Status: {response.status_code}")
    return response


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            error="Not Found",
            detail=f"The requested path '{request.url.path}' does not exist",
            timestamp=datetime.now()
        ).model_dump(mode='json')
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Custom 500 handler"""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal Server Error",
            detail="An unexpected error occurred. Please try again.",
            timestamp=datetime.now()
        ).model_dump(mode='json')
    )


# ============================================================================
# ROUTES
# ============================================================================

app.include_router(router)


# ============================================================================
# STARTUP / SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("\n" + "="*80)
    print("🚀 PHARMA INTELLIGENCE API STARTING")
    print("="*80)
    print(f"Version: {app.version}")
    print(f"Docs: http://localhost:8000/docs")
    print(f"Time: {datetime.now().isoformat()}")
    print("="*80 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print("\n" + "="*80)
    print("🛑 PHARMA INTELLIGENCE API SHUTTING DOWN")
    print("="*80 + "\n")


# ============================================================================
# MAIN (for direct execution)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*80)
    print("PHARMA INTELLIGENCE API - DEV SERVER")
    print("="*80)
    print("\n⚠️  Running in development mode")
    print("For production, use: uvicorn api.main:app --host 0.0.0.0 --port 8000\n")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
