
from playwright.sync_api import sync_playwright
import time

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Go to the app root
    page.goto("http://localhost:8080")

    # Handle Age Gate
    try:
        page.wait_for_selector("#age-gate-enter", timeout=5000)
        print("Clicking Age Gate Enter button...")
        page.click("#age-gate-enter")
    except Exception as e:
        print(f"Age gate not found or error: {e}")

    # Wait for app to initialize by waiting for the main nav
    page.wait_for_selector("#main-nav", timeout=10000)

    # Mock the admin user state and navigate
    print("Mocking admin user...")
    page.evaluate("""() => {
        if (!window.app) {
            console.error("window.app is not defined!");
            return;
        }

        // Mock user
        const mockUser = {
            uid: 'test_admin_uid',
            email: 'darkdesire389@gmail.com',
            getIdToken: async () => 'mock_token'
        };

        window.app.user = mockUser;
        window.app.userProfile = {
            email: 'darkdesire389@gmail.com',
            isAdmin: true,
            firstName: 'Admin',
            lastName: 'User'
        };
        window.app.authReady = true;

        // Force update UI based on auth state
        window.app.updateAuthUI(true);

        // Navigate to admin
        window.location.hash = '/admin';
        // Manually trigger render if hash change doesn't pick it up immediately (though it should)
        window.app.renderPage();
    }""")

    # Wait for the admin page to render
    print("Waiting for admin form...")
    try:
        # Wait for the specific element we want to verify
        page.wait_for_selector("#aliexpress-integration-section", timeout=10000)
        print("AliExpress section found.")
    except Exception as e:
        print(f"Timeout waiting for admin form. Current URL: {page.url}")
        page.screenshot(path="/home/jules/verification/debug_timeout_retry.png")
        raise e

    # Scroll to the AliExpress section to ensure it's visible in screenshot
    page.locator("#aliexpress-integration-section").scroll_into_view_if_needed()

    # Take a screenshot of the AliExpress section
    page.screenshot(path="/home/jules/verification/aliexpress_admin_ui.png", full_page=True)
    print("Screenshot taken.")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
