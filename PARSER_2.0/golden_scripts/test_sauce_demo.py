import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.locator("body").click()
    page.goto("https://www.saucedemo.com/v1/")
    page.locator("[data-test=\"username\"]").click()
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").click()
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.get_by_role("button", name="LOGIN").click()
    page.locator("div").filter(has_text=re.compile(r"^\$29\.99ADD TO CART$")).get_by_role("button").click()
    page.get_by_role("button", name="ADD TO CART").nth(1).click()
    page.locator("div").filter(has_text=re.compile(r"^\$7\.99ADD TO CART$")).get_by_role("button").click()
    page.locator("div").filter(has_text=re.compile(r"^\$15\.99ADD TO CART$")).get_by_role("button").click()
    page.locator("div").filter(has_text=re.compile(r"^\$49\.99ADD TO CART$")).get_by_role("button").click()
    page.get_by_role("button", name="ADD TO CART").click()
    page.get_by_role("link", name="6").click()
    page.get_by_role("link", name="CHECKOUT").click()
    page.locator("[data-test=\"firstName\"]").click()
    page.locator("[data-test=\"firstName\"]").fill("Ali")
    page.locator("[data-test=\"firstName\"]").press("Tab")
    page.locator("[data-test=\"lastName\"]").fill("Khan")
    page.locator("[data-test=\"lastName\"]").press("Tab")
    page.locator("[data-test=\"postalCode\"]").fill("7500")
    page.get_by_role("button", name="CONTINUE").click()
    expect(page.locator("#checkout_summary_container")).to_contain_text("FREE PONY EXPRESS DELIVERY!")
    page.get_by_role("link", name="FINISH").click()
    expect(page.get_by_role("heading")).to_contain_text("THANK YOU FOR YOUR ORDER")
    expect(page.locator("#checkout_complete_container")).to_contain_text("Your order has been dispatched, and will "
                                                                         "arrive just as fast as the pony can get "
                                                                         "there!")
    page.get_by_role("button", name="Open Menu").click()
    page.get_by_role("link", name="Logout").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
