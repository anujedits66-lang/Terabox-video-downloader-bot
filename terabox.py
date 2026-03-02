import re
import logging
from curl_cffi import requests as cffi_requests

from config import NDUS_COOKIE

logger = logging.getLogger(__name__)

_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 Chrome/145.0.0.0 Safari/537.36"
)


def _make_session() -> cffi_requests.Session:
    session = cffi_requests.Session(impersonate="chrome110")
    session.cookies.update({"ndus": NDUS_COOKIE})
    return session


def fetch_file_list(surl: str) -> dict:
    short_url = surl[1:] if surl.startswith("1") else surl
    session   = _make_session()
    headers   = {"User-Agent": _UA}

    first_url = f"https://dm.terabox.app/sharing/link?surl={surl}"
    logger.debug("Fetching share page: %s", first_url)

    try:
        resp = session.get(first_url, headers=headers, timeout=20)
        resp.raise_for_status()
    except Exception as exc:
        logger.error("Failed to fetch share page: %s", exc)
        return {"error": f"Could not reach TeraBox: {exc}"}

    match = re.search(r'fn%28%22(.*?)%22%29', resp.text)
    if not match:
        logger.warning("jsToken not found in share page HTML")
        return {"error": "Could not extract jsToken. Link may be invalid, expired, or Cloudflare blocked."}

    js_token = match.group(1)
    logger.debug("Extracted jsToken: %s", js_token)

    api_headers = {
        "Host": "dm.terabox.app",
        "User-Agent": _UA,
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": f"https://dm.terabox.app/sharing/link?surl={short_url}&clearCache=1",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://dm.terabox.app",
    }
    params = {
        "app_id": "250528",
        "jsToken": js_token,
        "site_referer": "https://www.terabox.app/",
        "shorturl": short_url,
        "root": "1",
    }

    try:
        api_resp = session.get(
            "https://dm.terabox.app/share/list",
            params=params,
            headers=api_headers,
            timeout=20,
        )
        api_resp.raise_for_status()
        return api_resp.json()
    except Exception as exc:
        logger.error("share/list API call failed: %s", exc)
        return {"error": f"API request failed: {exc}"}
