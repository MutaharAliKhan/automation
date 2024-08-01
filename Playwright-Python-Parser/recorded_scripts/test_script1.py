from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) ->None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.wait_for_timeout(1000)
    page.goto('https://practicetestautomation.com/practice-test-login/')
    page.get_by_label('Username').fill('value1')
    page.get_by_label('Username').fill('value2')
    page.locator('#password').fill('value3')
    page.locator('#password').fill('value4')
    # sdasdasdasdsa
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').fill('value5')
    page.locator('data-e2e="add-to-cart-sauce-labs-backpack"]').fill('value6')
    page.check('//a[usernmae="standard_user"]').fill("value7")
    page.locator('[data-test="submit"]').fill("value8")
    page.locator('[data-e2e="submit"]').fill("value9")
    page.locator("input[name='password']").fill("value10")
    page.fill("input[name='password']", "value11")
    page.fill("input[name='password']", "value12")
    page.wait_for_timeout(1000)
    # sdasdasdasdsa
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
