import time
import logging
from typing import Any

from config import CACHE_TTL

logger  = logging.getLogger(__name__)
_store: dict[str, tuple[Any, float]] = {}


def get(surl: str) -> Any | None:
    entry = _store.get(surl)
    if entry is None:
        return None
    data, expiry = entry
    if time.time() > expiry:
        logger.debug("Cache expired: %s", surl)
        del _store[surl]
        return None
    logger.debug("Cache hit: %s", surl)
    return data


def set(surl: str, data: Any) -> None:
    _store[surl] = (data, time.time() + CACHE_TTL)
    logger.debug("Cached: %s (TTL=%ds)", surl, CACHE_TTL)


def clear() -> None:
    _store.clear()
