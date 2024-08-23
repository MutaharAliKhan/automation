import random
import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # comment
    page.get_by_text('testing1').click()
    page.get_by_text('testing2').press("Enter")
    page.get_by_text('ABC').fill('XYZ')
    page.get_by_text('ABC').fill('XYZ')
    page.get_by_text('ABC').fill('XYZ')
    page.locator('#button').filter(has_text="dasdasd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.get_by_text('Submit').click()
    page.get_by_text('Cancel').click()
    page.get_by_text('Cancel').click()
    page.get_by_text('Cancel').click()
    page.get_by_text('Cancel').click()
    page.get_by_text('Cancel').click()
    page.get_by_text('Cancel').click()
    expect(page.get_by_text('Welcome').to_be_visible())
    expect(page.get_by_text('Welcome').to_be_visible())
    expect(page.get_by_text('Welcome').to_be_visible())
    expect(page.get_by_text('Welcome').to_be_visible())
    expect(page.get_by_text('Welcome').to_be_visible())
    expect(page.get_by_text('Welcome').to_be_visible())
    expect(page.get_by_text('Welcome').to_be_visible())
    expect(page.get_by_text('Welcome').to_be_visible())
    expect(page.get_by_text('Welcome').to_be_visible())
    expect(page.get_by_text('Welcome').to_be_visible())
    expect(page.get_by_text('Welcome').to_be_visible())
    expect(page.get_by_text('Welcome').to_be_visible())
    expect(page.get_by_text('Welcome').to_be_visible())


    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
