# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp<2", "camoufox[geoip]"]
# ///
"""
Camoufox MCP server — thin, self-contained wrapper around the official
daijro/camoufox Python library (anti-detect Firefox on Playwright).

No third-party MCP wrapper exists for Camoufox (verified against the
official repo directly), so this is written in-house against the
official `camoufox` pip package only. One persistent browser/page per
server process; tools operate on that single page.
"""

import asyncio
from typing import Optional

from mcp.server.fastmcp import FastMCP
from camoufox.async_api import AsyncCamoufox

mcp = FastMCP("camoufox")

_camoufox_cm = None
_browser = None
_page = None
_lock = asyncio.Lock()


async def _ensure_page(headless: bool = True):
    global _camoufox_cm, _browser, _page
    async with _lock:
        if _page is not None:
            return _page
        _camoufox_cm = AsyncCamoufox(headless=headless, geoip=True)
        _browser = await _camoufox_cm.__aenter__()
        _page = await _browser.new_page()
        return _page


@mcp.tool()
async def camoufox_navigate(url: str, headless: bool = True) -> str:
    """Open (or reuse) the Camoufox browser and navigate to a URL. Returns the final URL and page title."""
    page = await _ensure_page(headless=headless)
    await page.goto(url, wait_until="load")
    title = await page.title()
    return f"url={page.url} title={title!r}"


@mcp.tool()
async def camoufox_content() -> str:
    """Return the current page's visible text content (not raw HTML)."""
    if _page is None:
        return "error: no page open, call camoufox_navigate first"
    text = await _page.inner_text("body")
    return text[:20000]


@mcp.tool()
async def camoufox_screenshot(path: str, full_page: bool = True) -> str:
    """Save a screenshot of the current page to an absolute file path. Returns the path."""
    if _page is None:
        return "error: no page open, call camoufox_navigate first"
    await _page.screenshot(path=path, full_page=full_page)
    return path


@mcp.tool()
async def camoufox_click(selector: str) -> str:
    """Click the first element matching a CSS selector."""
    if _page is None:
        return "error: no page open, call camoufox_navigate first"
    await _page.click(selector, timeout=10000)
    return f"clicked {selector!r}"


@mcp.tool()
async def camoufox_fill(selector: str, value: str) -> str:
    """Fill a form field (input/textarea) matching a CSS selector with a value."""
    if _page is None:
        return "error: no page open, call camoufox_navigate first"
    await _page.fill(selector, value, timeout=10000)
    return f"filled {selector!r}"


@mcp.tool()
async def camoufox_evaluate(js: str) -> str:
    """Run JavaScript in the page context and return the JSON-serializable result as a string."""
    if _page is None:
        return "error: no page open, call camoufox_navigate first"
    result = await _page.evaluate(js)
    return str(result)


@mcp.tool()
async def camoufox_close() -> str:
    """Close the browser and release resources. Call when done with a session."""
    global _camoufox_cm, _browser, _page
    async with _lock:
        if _camoufox_cm is not None:
            await _camoufox_cm.__aexit__(None, None, None)
        _camoufox_cm = None
        _browser = None
        _page = None
    return "closed"


if __name__ == "__main__":
    mcp.run()
