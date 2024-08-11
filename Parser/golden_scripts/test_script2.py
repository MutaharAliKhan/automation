import random

from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) ->None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.locator("branch_code").fill("1026")
    page.locator("username").fill("VQATST1")
    page.locator("password").fill("login11111")
    page.locator("narration").fill("TESTING")
    page.locator("payslip").fill("12345")
    page.locator("cnic").fill("42201-1234567-1")
    page.locator("amount").fill("50000")
    page.locator("receipt").fill("54321")
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
