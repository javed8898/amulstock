#!/usr/bin/env python3
"""
Amul product stock checker — checks multiple products and sends a Telegram
message the moment any of them come back in stock.

Designed to run on a schedule (GitHub Actions, cron, Task Scheduler, etc).
"""

import requests
import sys
import os

PRODUCTS = [
    {
        "name": "Amul Whey Protein, 32g | Pack of 60 Sachets",
        "url": "https://shop.amul.com/en/product/amul-kool-protein-milkshake-or-kesar-180-ml-or-pack-of-8",
    },
    {
        "name": "Amul Chocolate Whey Protein, 34g | Pack of 60 Sachets",
        "url": "https://shop.amul.com/en/product/amul-chocolate-whey-protein-34-g-or-pack-of-60-sachets",
    },
]

# --- Telegram config: set these as environment variables / GitHub secrets ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}


def is_in_stock(url: str) -> bool:
    resp = requests.get(url, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    html = resp.text

    # The page shows "Sold Out" near the buy button when unavailable,
    # and an active "Add to Cart" button when available.
    if "Sold Out" in html:
        return False
    if "Add to Cart" in html:
        return True

    print(f"Warning: could not determine stock status reliably for {url}", file=sys.stderr)
    return False


def send_telegram_alert(name: str, url: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials not set. Skipping notification, printing instead.")
        print(f"IN STOCK: {name} -> {url}")
        return

    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    message = f"🟢 IN STOCK: {name}\nGrab it now: {url}"
    r = requests.post(api_url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})
    r.raise_for_status()


def main():
    any_error = False
    for product in PRODUCTS:
        try:
            if is_in_stock(product["url"]):
                print(f"IN STOCK: {product['name']} — sending alert.")
                send_telegram_alert(product["name"], product["url"])
            else:
                print(f"Still out of stock: {product['name']}")
        except requests.RequestException as e:
            print(f"Error checking {product['name']}: {e}", file=sys.stderr)
            any_error = True

    if any_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
