"""HTTP fetch utilities returning lxml HTML trees."""

from logging import getLogger

import requests
from lxml import html
from lxml.html import HtmlElement

from ..cache import fetch_with_cache

logger = getLogger("html")


def _fetch_html(url: str) -> bytes:
    x = requests.get(url, timeout=30)
    return x.content


def get_html_tree(url: str) -> HtmlElement:
    """Fetch a URL and return the content as an lxml HTML element tree."""
    try:
        content = fetch_with_cache(url, _fetch_html)
        return html.fromstring(content)
    except (requests.RequestException, ValueError):
        logger.exception(f"Error fetching {url}")
        raise


if __name__ == "__main__":
    pass
