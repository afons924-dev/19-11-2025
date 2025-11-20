
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Go to the app root
    page.goto("http://localhost:8080")

    # Handle Age Gate
    try:
        if page.is_visible("#age-gate-enter"):
            print("Clicking Age Gate Enter button...")
            page.click("#age-gate-enter")
    except Exception as e:
        print(f"Error handling age gate: {e}")

    # Wait for app to initialize
    # Look for the main header or app-root content
    try:
        page.wait_for_selector("header", timeout=5000)
    except:
        print("Timeout waiting for header.")

    # Wait a bit for JS execution
    page.wait_for_timeout(2000)

    # Mock the admin user state and navigate
    page.evaluate("""() => {
        if (!window.app) {
            console.error("window.app is not defined!");
            return;
        }
        window.app.user = {
            uid: 'test_admin_uid',
            email: 'darkdesire389@gmail.com'
        };
        window.app.userProfile = {
            email: 'darkdesire389@gmail.com',
            isAdmin: true,
            firstName: 'Admin',
            lastName: 'User'
        };
        window.app.authReady = true;

        // Force navigation to admin
        window.app.navigateTo('/admin');
    }""")

    # Wait for the admin page to render
    try:
        page.wait_for_selector("#admin-product-form", timeout=10000)
        print("Admin form found.")
    except:
        print(f"Timeout waiting for admin form. Current URL: {page.url}")
        page.screenshot(path="/home/jules/verification/debug_timeout_2.png")
        raise

    # Scroll to the AliExpress section
    aliexpress_section = page.locator("#aliexpress-integration-section")
    if aliexpress_section.count() > 0:
        aliexpress_section.scroll_into_view_if_needed()
        print("AliExpress section found.")
    else:
        print("AliExpress section NOT found.")

    # Take a screenshot of the AliExpress section
    page.screenshot(path="/home/jules/verification/aliexpress_admin_ui.png", full_page=True)

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
