import random
import time
from typing import Dict, List

from playwright.sync_api import sync_playwright

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


def search_marketplace(keyword: str, location: str, radius_km: int) -> List[Dict[str, str]]:
    """Scrape Facebook Marketplace for listings.

    NOTE: Facebook may block automated access and may require login.
    Ensure you comply with Facebook's Terms of Service.
    """
    user_agent = random.choice(USER_AGENTS)
    delay = random.uniform(2, 5)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()

        url = (
            "https://www.facebook.com/marketplace/"
            f"{location}/search?query={keyword}&radius_km={radius_km}"
        )
        page.goto(url, wait_until="domcontentloaded")
        time.sleep(delay)

        listings: List[Dict[str, str]] = []
        for item in page.query_selector_all("div[role='article']"):
            title_el = item.query_selector("span")
            price_el = item.query_selector("span[dir='auto']")
            link_el = item.query_selector("a")

            if not (title_el and price_el and link_el):
                continue

            listings.append(
                {
                    "id": link_el.get_attribute("href") or "",
                    "title": title_el.inner_text(),
                    "price": price_el.inner_text(),
                    "link": link_el.get_attribute("href") or "",
                }
            )

        browser.close()
        return listings
