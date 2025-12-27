import random
import time
from typing import Dict, List

from playwright.sync_api import sync_playwright

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


def extract_listings(page) -> List[Dict[str, str]]:
    """Extract listings from the page using DOM evaluation."""
    return page.evaluate("""
        () => {
            const listings = [];
            const items = document.querySelectorAll("div[role='article']");
            for (const item of items) {
                const titleEl = item.querySelector("span");
                const priceEl = item.querySelector("span[dir='auto']");
                const linkEl = item.querySelector("a");

                if (!titleEl || !priceEl || !linkEl) continue;

                listings.push({
                    "id": linkEl.getAttribute("href") || "",
                    "title": titleEl.innerText,
                    "price": priceEl.innerText,
                    "link": linkEl.getAttribute("href") || ""
                });
            }
            return listings;
        }
    """)


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

        listings = extract_listings(page)

        browser.close()
        return listings
