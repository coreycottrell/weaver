"""
Bluesky Rate Limiter - Handles rate limiting for API operations

Rate Limits (as of 2025):
- 5,000 points per hour
- 35,000 points per day
- Create operations = 3 points
- Update operations = 2 points
- Delete operations = 1 point

Login Rate Limits:
- 30 per 5 minutes per handle
- 300 per day per handle
- 10 per day per IP (for fresh logins!)

This module helps you stay within these limits.
"""

import time
import json
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional
from collections import deque


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""
    points_per_hour: int = 5000
    points_per_day: int = 35000
    create_points: int = 3
    update_points: int = 2
    delete_points: int = 1
    
    # Safety margins (use 90% of limits to be safe)
    safety_margin: float = 0.9
    
    @property
    def safe_points_per_hour(self) -> int:
        return int(self.points_per_hour * self.safety_margin)
    
    @property
    def safe_points_per_day(self) -> int:
        return int(self.points_per_day * self.safety_margin)


@dataclass
class RateLimitStats:
    """Track rate limit statistics."""
    points_used_hour: int = 0
    points_used_day: int = 0
    hour_start: datetime = field(default_factory=datetime.utcnow)
    day_start: datetime = field(default_factory=lambda: datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0
    ))
    operations: deque = field(default_factory=lambda: deque(maxlen=10000))


class RateLimiter:
    """
    Rate limiter for Bluesky API operations.
    
    Tracks points used and automatically waits when approaching limits.
    """
    
    def __init__(
        self,
        config: Optional[RateLimitConfig] = None,
        stats_file: str = "rate_limit_stats.json"
    ):
        self.config = config or RateLimitConfig()
        self.stats_file = Path(stats_file)
        self.stats = self._load_stats()
        self._cleanup_old_operations()
    
    def _load_stats(self) -> RateLimitStats:
        """Load rate limit stats from file."""
        try:
            if self.stats_file.exists():
                with open(self.stats_file, 'r') as f:
                    data = json.load(f)
                    return RateLimitStats(
                        points_used_hour=data.get('points_used_hour', 0),
                        points_used_day=data.get('points_used_day', 0),
                        hour_start=datetime.fromisoformat(data['hour_start']),
                        day_start=datetime.fromisoformat(data['day_start']),
                        operations=deque(
                            [(datetime.fromisoformat(op['time']), op['points']) 
                             for op in data.get('operations', [])],
                            maxlen=10000
                        )
                    )
        except (json.JSONDecodeError, IOError, KeyError):
            pass
        return RateLimitStats()
    
    def _save_stats(self) -> None:
        """Save rate limit stats to file."""
        try:
            data = {
                'points_used_hour': self.stats.points_used_hour,
                'points_used_day': self.stats.points_used_day,
                'hour_start': self.stats.hour_start.isoformat(),
                'day_start': self.stats.day_start.isoformat(),
                'operations': [
                    {'time': op[0].isoformat(), 'points': op[1]}
                    for op in list(self.stats.operations)[-1000:]  # Keep last 1000
                ]
            }
            with open(self.stats_file, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            print(f"[WARNING] Could not save rate limit stats: {e}")
    
    def _cleanup_old_operations(self) -> None:
        """Remove operations older than 24 hours and recalculate stats."""
        now = datetime.utcnow()
        hour_ago = now - timedelta(hours=1)
        day_ago = now - timedelta(days=1)
        
        # Filter operations within time windows
        hour_ops = [(t, p) for t, p in self.stats.operations if t > hour_ago]
        day_ops = [(t, p) for t, p in self.stats.operations if t > day_ago]
        
        self.stats.points_used_hour = sum(p for _, p in hour_ops)
        self.stats.points_used_day = sum(p for _, p in day_ops)
        self.stats.operations = deque(day_ops, maxlen=10000)
        
        # Reset hour/day start if needed
        if (now - self.stats.hour_start).total_seconds() > 3600:
            self.stats.hour_start = now
            self.stats.points_used_hour = 0
        
        if (now - self.stats.day_start).total_seconds() > 86400:
            self.stats.day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            self.stats.points_used_day = 0
    
    def _record_operation(self, points: int) -> None:
        """Record an operation."""
        now = datetime.utcnow()
        self.stats.operations.append((now, points))
        self.stats.points_used_hour += points
        self.stats.points_used_day += points
        self._save_stats()
    
    def can_proceed(self, points: int) -> bool:
        """Check if we can proceed with an operation of given points."""
        self._cleanup_old_operations()
        
        hour_ok = (self.stats.points_used_hour + points) <= self.config.safe_points_per_hour
        day_ok = (self.stats.points_used_day + points) <= self.config.safe_points_per_day
        
        return hour_ok and day_ok
    
    def wait_if_needed(self, points: int) -> float:
        """
        Wait if necessary before proceeding with an operation.
        
        Returns:
            float: Seconds waited (0 if no wait was needed)
        """
        self._cleanup_old_operations()
        
        wait_time = 0.0
        
        # Check hourly limit
        if (self.stats.points_used_hour + points) > self.config.safe_points_per_hour:
            # Wait until hour resets
            elapsed = (datetime.utcnow() - self.stats.hour_start).total_seconds()
            remaining = max(0, 3600 - elapsed)
            wait_time = max(wait_time, remaining)
            print(f"[RATE LIMIT] Hourly limit reached. Waiting {remaining:.0f}s...")
        
        # Check daily limit
        if (self.stats.points_used_day + points) > self.config.safe_points_per_day:
            # Wait until day resets
            now = datetime.utcnow()
            tomorrow = (now + timedelta(days=1)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            remaining = (tomorrow - now).total_seconds()
            wait_time = max(wait_time, remaining)
            print(f"[RATE LIMIT] Daily limit reached. Waiting {remaining:.0f}s...")
        
        if wait_time > 0:
            time.sleep(wait_time)
            self._cleanup_old_operations()
        
        return wait_time
    
    def record_create(self) -> None:
        """Record a create operation (3 points)."""
        self._record_operation(self.config.create_points)
    
    def record_update(self) -> None:
        """Record an update operation (2 points)."""
        self._record_operation(self.config.update_points)
    
    def record_delete(self) -> None:
        """Record a delete operation (1 point)."""
        self._record_operation(self.config.delete_points)
    
    def get_status(self) -> dict:
        """Get current rate limit status."""
        self._cleanup_old_operations()
        return {
            'points_used_hour': self.stats.points_used_hour,
            'points_remaining_hour': self.config.safe_points_per_hour - self.stats.points_used_hour,
            'points_used_day': self.stats.points_used_day,
            'points_remaining_day': self.config.safe_points_per_day - self.stats.points_used_day,
            'creates_remaining_hour': (self.config.safe_points_per_hour - self.stats.points_used_hour) // 3,
            'creates_remaining_day': (self.config.safe_points_per_day - self.stats.points_used_day) // 3,
        }
    
    def print_status(self) -> None:
        """Print current rate limit status."""
        status = self.get_status()
        print("\n📊 Rate Limit Status:")
        print(f"   Hourly: {status['points_used_hour']}/{self.config.safe_points_per_hour} points used")
        print(f"   Daily:  {status['points_used_day']}/{self.config.safe_points_per_day} points used")
        print(f"   Creates remaining (hour): ~{status['creates_remaining_hour']}")
        print(f"   Creates remaining (day):  ~{status['creates_remaining_day']}")


# Global rate limiter instance
_rate_limiter: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance."""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter


if __name__ == "__main__":
    # Test the rate limiter
    print("Testing Rate Limiter...")
    print("=" * 50)
    
    limiter = RateLimiter()
    limiter.print_status()
    
    # Simulate some operations
    print("\nSimulating 5 create operations...")
    for i in range(5):
        limiter.wait_if_needed(3)
        limiter.record_create()
        print(f"   Operation {i+1} recorded")
    
    limiter.print_status()
