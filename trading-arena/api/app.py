"""
Trading Arena API - FastAPI Entry Point

AI-CIV Trading Arena Phase 1
Ed25519-authenticated REST API for multi-collective paper trading.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import health, collectives, orders, portfolio, audit


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup/shutdown events."""
    import os
    from .db import init_db, close_db

    # Startup
    print("Trading Arena API starting up...")

    # Initialize database connection
    try:
        # In development, create tables automatically if CREATE_TABLES=true
        create_tables = os.environ.get("CREATE_TABLES", "").lower() == "true"
        echo_sql = os.environ.get("ECHO_SQL", "").lower() == "true"

        await init_db(create_tables=create_tables, echo=echo_sql)
        print("Database connection initialized")
    except ValueError as e:
        # DATABASE_URL not set - continue without database for development
        print(f"Warning: {e}")
        print("Running without database connection (in-memory mode)")

    yield

    # Shutdown
    print("Trading Arena API shutting down...")
    await close_db()
    print("Database connection closed")


app = FastAPI(
    title="AI-CIV Trading Arena",
    description="Multi-collective paper trading platform with Ed25519 authentication",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    openapi_url="/v1/openapi.json",
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include route modules
app.include_router(health.router, prefix="/v1", tags=["Health"])
app.include_router(collectives.router, prefix="/v1/collectives", tags=["Collectives"])
app.include_router(orders.router, prefix="/v1/orders", tags=["Orders"])
app.include_router(portfolio.router, prefix="/v1/portfolio", tags=["Portfolio"])
app.include_router(audit.router, prefix="/v1/audit", tags=["Audit"])


@app.get("/")
async def root():
    """Root endpoint - redirect to API documentation."""
    return {
        "message": "AI-CIV Trading Arena API",
        "version": "1.0.0",
        "docs": "/v1/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
