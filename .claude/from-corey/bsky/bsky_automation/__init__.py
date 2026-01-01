"""
Bluesky Automation Toolkit

A complete toolkit for automating Bluesky social media activities.

Updated for 2025 using the official atproto Python SDK.
"""

__version__ = "2.0.0"
__author__ = "Corey Cottrell"

from .session_manager import BlueskySessionManager, get_client
from .rate_limiter import RateLimiter, get_rate_limiter
from .ai_responder import AIResponder, create_responder

__all__ = [
    'BlueskySessionManager',
    'get_client',
    'RateLimiter',
    'get_rate_limiter',
    'AIResponder',
    'create_responder',
]
