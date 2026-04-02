from __future__ import annotations

import asyncio
import functools
from typing import Callable, TypeVar

from agentcore.exceptions import RateLimitError

T = TypeVar("T")

RETRYABLE_EXCEPTIONS = (RateLimitError, ConnectionError, TimeoutError)


def with_retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator that retries an async function on transient failures.

    Only retries on RateLimitError, ConnectionError, and TimeoutError.
    All other exceptions propagate immediately.
    After exhausting retries, re-raises the last exception.
    """
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            last_exc = None
            current_delay = delay
            for attempt in range(max_attempts):
                try:
                    return await fn(*args, **kwargs)
                except RETRYABLE_EXCEPTIONS as exc:
                    last_exc = exc
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
            raise last_exc
        return wrapper
    return decorator
