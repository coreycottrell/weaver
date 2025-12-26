"""
Health and System Endpoints

GET /v1/health - System health check
GET /v1/symbols - Available trading symbols
"""

from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    System health check (public endpoint).
    
    Returns current system status and service health.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "services": {
            "database": "healthy",  # TODO: Implement actual checks
            "order_engine": "healthy",
            "market_data": "healthy"
        }
    }


@router.get("/symbols")
async def list_symbols():
    """
    List available trading symbols (public endpoint).
    
    Returns all symbols available for paper trading.
    """
    # Phase 1: Static symbol list
    # TODO: Load from database/config in later phases
    return {
        "symbols": [
            {
                "symbol": "SOL/USDC",
                "base_currency": "SOL",
                "quote_currency": "USDC",
                "status": "trading",
                "min_quantity": 0.01,
                "max_quantity": 10000.0,
                "quantity_precision": 2,
                "price_precision": 4,
                "min_notional": 1.0
            },
            {
                "symbol": "ETH/USDC",
                "base_currency": "ETH",
                "quote_currency": "USDC",
                "status": "trading",
                "min_quantity": 0.001,
                "max_quantity": 1000.0,
                "quantity_precision": 3,
                "price_precision": 2,
                "min_notional": 1.0
            },
            {
                "symbol": "BTC/USDC",
                "base_currency": "BTC",
                "quote_currency": "USDC",
                "status": "trading",
                "min_quantity": 0.0001,
                "max_quantity": 100.0,
                "quantity_precision": 4,
                "price_precision": 2,
                "min_notional": 1.0
            }
        ]
    }
