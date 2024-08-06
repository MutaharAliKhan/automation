from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) ->None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.99acres.com/login")
    page.goto("https://www.99acres.com/login")
    page.goto("https://www.99acres.com/login")
    page.goto("https://www.99acres.com/login")
    page.goto("https://www.99acres.com/login")
    page.goto("https://www.99acres.com/login")
    page.goto("https://www.99acres.com/login")
    page.goto("https://www.99acres.com/login")
    page.get_by_label('branch_code').fill('1026')
    page.get_by_label('username').fill('TESTING')
    page.get_by_label('password').fill('TESTING1')
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
