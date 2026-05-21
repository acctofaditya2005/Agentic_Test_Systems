from playwright.sync_api import sync_playwright, expect

def test_page_loads():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()
        page.goto("http://localhost:8000")
        title = page.title()
        print(f"Page title: {title}")

        assert "Drum Kit" in title
        browser.close()

def test_all_buttons_exist():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()
        page.goto("http://localhost:8000")

        drums = page.locator(".drum")
        expect(drums).to_have_count(7)
        browser.close()

def test_buttons_labels():
    with sync_playwright() as p:
        browser =p.chromium.launch(headless = True)
        page = browser.new_page()
        page.goto("http://localhost:8000")
        labels = ['w','a','s','d','j','k','l']
        for label in labels:
            button = page.locator(f"button.{label}")
            assert button.text_content() == label
        browser.close()

def test_click_button():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()
        page.goto("http://localhost:8000")
        page.locator(".w").click()
        assert page.title() == "Drum Kit"
        browser.close()

def test_wrong_button_count():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()
        page.goto("http://localhost:8000")
        drums = page.locator(".drum")
        expect(drums).to_have_count(10)
        browser.close()

def test_broken_selector():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()
        page.goto("http://localhost:8000")
        button = page.locator(".drum-k")
        button.click(timeout=3000)
        browser.close()


       
