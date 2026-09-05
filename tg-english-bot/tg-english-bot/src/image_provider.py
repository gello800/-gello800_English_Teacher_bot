"""Finds a contextual image for a word via the Unsplash API (optional)."""
import requests
from . import config


def get_image_url(query: str):
    if not config.ENABLE_IMAGES:
        return None
    try:
        resp = requests.get(
            "https://api.unsplash.com/search/photos",
            params={"query": query, "per_page": 1, "orientation": "landscape"},
            headers={"Authorization": f"Client-ID {config.UNSPLASH_ACCESS_KEY}"},
            proxies=config.PROXIES,
            timeout=10,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if not results:
            return None
        return results[0]["urls"]["regular"]
    except requests.RequestException:
        return None
