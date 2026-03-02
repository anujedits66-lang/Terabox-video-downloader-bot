import re
from urllib.parse import urlparse, parse_qs

ALLOWED_HOSTS = {
    "terabox.app",      "www.terabox.app",
    "teraboxshare.com", "www.teraboxshare.com",
    "terabox.com",      "www.terabox.com",
    "1024terabox.com",  "www.1024terabox.com",
    "teraboxlink.com",  "www.teraboxlink.com",
    "dm.terabox.app",
}


def is_valid_terabox_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return False
        if (parsed.hostname or "").lower() not in ALLOWED_HOSTS:
            return False
        return "/s/" in parsed.path or "surl" in parsed.query
    except Exception:
        return False


def extract_surl(url: str) -> str | None:
    try:
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        if "surl" in qs:
            return qs["surl"][0]
        match = re.search(r"/s/([a-zA-Z0-9_-]+)", parsed.path)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None


def find_url_in_text(text: str) -> str | None:
    match = re.search(r"https?://\S+", text)
    return match.group(0) if match else None
