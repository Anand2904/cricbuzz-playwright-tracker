import os
from datetime import datetime
from playwright.sync_api import sync_playwright

def run_tracker():
    # Create a folder to store your screenshots
    os.makedirs("screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        print("1. Opening Cricbuzz...")
        page.goto("https://www.cricbuzz.com/", wait_until="domcontentloaded")

        print("2. Navigating to Live Scores...")
        page.get_by_role("link", name="Live Scores", exact=True).click()
        page.wait_for_load_state("domcontentloaded")

        print("3. Opening the first live match scorecard...")
        scorecard_link = page.get_by_role("link", name="Scorecard").first
        scorecard_link.wait_for(state="visible", timeout=10000)
        scorecard_link.click()
        page.wait_for_load_state("domcontentloaded")

        # Wait briefly for scorecard elements to settle
        page.wait_for_timeout(2000)

        # 4. Extract Match Title & Live Status
        match_title = page.locator("h1").first.inner_text().strip()
        
        # Grab the red/blue status line (e.g., "Day 1: Stumps - Australia opt to bowl")
        status_locator = page.locator(
            "div.cb-text-stumps, div.cb-text-inprogress, div.cb-text-complete, "
            "div.cb-text-lunch, div.cb-text-tea, div.cb-text-rain, div.cb-scrcrd-status"
        ).first
        
        match_status = status_locator.inner_text().strip() if status_locator.count() > 0 else "Status unavailable"

        print("\n" + "=" * 60)
        print(f"MATCH  : {match_title}")
        print(f"STATUS : {match_status}")
        print("=" * 60)

        # 5. Take a timestamped screenshot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"screenshots/scorecard_{timestamp}.png"
        
        # Capture the visible scorecard viewport
        page.screenshot(path=screenshot_path, full_page=False)
        print(f"\nScreenshot saved to: {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    run_tracker()