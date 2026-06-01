"""HTTP response caching for ITU-T web data.

Caches raw HTML responses to avoid repeated network requests when
generating reports. Cache location defaults to ~/.cache/rapporteur-helper
and can be overridden via the RH_CACHE_DIR environment variable.
"""

from __future__ import annotations

import hashlib
import logging
import os
from collections.abc import Callable
from pathlib import Path

logger = logging.getLogger(__name__)

_DEFAULT_CACHE_DIR = Path.home() / ".cache" / "rapporteur-helper"


def get_cache_dir() -> Path:
    """Return the cache directory, respecting RH_CACHE_DIR env var."""
    cache_dir = Path(os.environ.get("RH_CACHE_DIR", str(_DEFAULT_CACHE_DIR)))
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def _url_to_key(url: str) -> str:
    """Generate a deterministic, filesystem-safe cache key from a URL."""
    return hashlib.sha256(url.encode()).hexdigest()


def get_cached(url: str) -> bytes | None:
    """Return cached response body for the given URL, or None if not cached."""
    cache_file = get_cache_dir() / f"{_url_to_key(url)}.html"
    if cache_file.exists():
        logger.debug("Cache hit: %s", url)
        return cache_file.read_bytes()
    logger.debug("Cache miss: %s", url)
    return None


def store_cached(url: str, content: bytes) -> Path:
    """Store response body in cache and return the cache file path."""
    cache_file = get_cache_dir() / f"{_url_to_key(url)}.html"
    cache_file.write_bytes(content)
    logger.debug("Cached: %s -> %s", url, cache_file)
    return cache_file


def fetch_with_cache(url: str, fetcher: Callable[[str], bytes]) -> bytes:
    """Fetch URL content, using cache if available.

    Args:
        url: The URL to fetch.
        fetcher: Callable that takes a URL and returns raw bytes.

    Returns:
        Raw bytes of the response body.
    """
    cached = get_cached(url)
    if cached is not None:
        return cached
    content = fetcher(url)
    store_cached(url, content)
    return content


def clear_cache() -> int:
    """Remove all cached files. Returns the number of files removed."""
    cache_dir = get_cache_dir()
    count = 0
    for f in cache_dir.glob("*.html"):
        f.unlink()
        count += 1
    logger.info("Cleared %d cached files from %s", count, cache_dir)
    return count
