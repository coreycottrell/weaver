#!/usr/bin/env python3
"""
Browser Vision Test - Demonstrates automated browser control and screenshot capture
"""
import os
from playwright.sync_api import sync_playwright
import time

def test_browser_vision():
    """Launch browser, take screenshots, click button, prove interaction"""

    html_path = os.path.abspath('test_browser_vision.html')
    screenshot_dir = os.path.dirname(html_path)

    print(f"📄 HTML file: {html_path}")
    print(f"📁 Screenshot directory: {screenshot_dir}")

    with sync_playwright() as p:
        # Launch browser (headless=False to see it, True for background)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # Navigate to our test page
        page.goto(f'file://{html_path}')
        print("✓ Browser launched and page loaded")

        # Wait for page to fully render
        time.sleep(1)

        # Take initial screenshot
        screenshot_before = os.path.join(screenshot_dir, 'screenshot_before_click.png')
        page.screenshot(path=screenshot_before)
        print(f"✓ Initial screenshot saved: {screenshot_before}")

        # Get initial state
        status_before = page.locator('#status').inner_text()
        clicks_before = page.locator('#clickCount').inner_text()
        print(f"  Status before: {status_before}")
        print(f"  {clicks_before}")

        # Click the button
        page.click('#testButton')
        print("✓ Button clicked!")

        # Wait for animation and state update
        time.sleep(0.5)

        # Take screenshot after click
        screenshot_after = os.path.join(screenshot_dir, 'screenshot_after_click.png')
        page.screenshot(path=screenshot_after)
        print(f"✓ Post-click screenshot saved: {screenshot_after}")

        # Get updated state to prove the click worked
        status_after = page.locator('#status').inner_text()
        clicks_after = page.locator('#clickCount').inner_text()
        print(f"  Status after: {status_after}")
        print(f"  {clicks_after}")

        # Click a few more times to really prove it
        for i in range(2, 5):
            page.click('#testButton')
            time.sleep(0.3)

        clicks_final = page.locator('#clickCount').inner_text()
        print(f"  Final count: {clicks_final}")

        # Take final screenshot
        screenshot_final = os.path.join(screenshot_dir, 'screenshot_multiple_clicks.png')
        page.screenshot(path=screenshot_final)
        print(f"✓ Final screenshot saved: {screenshot_final}")

        # Keep browser open for a moment to see it
        time.sleep(2)

        browser.close()
        print("✓ Browser closed")

        print("\n" + "="*60)
        print("PROOF OF INTERACTION:")
        print("="*60)
        print(f"Before click: {status_before} | {clicks_before}")
        print(f"After click:  {status_after} | {clicks_after}")
        print(f"After more:   {clicks_final}")
        print("="*60)
        print(f"\nScreenshots available at:")
        print(f"  1. {screenshot_before}")
        print(f"  2. {screenshot_after}")
        print(f"  3. {screenshot_final}")

if __name__ == '__main__':
    test_browser_vision()
