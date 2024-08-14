import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://adactinhotelapp.com/HotelAppBuild2/")
    page.locator("#username").click()
    page.locator("#username").fill("Admin001")
    page.locator("#password").click()
    page.locator("#password").fill("N0C6LN")
    page.get_by_role("button", name="Login").click()

    page.locator("#location").select_option("Sydney")
    page.locator("#hotels").select_option("Hotel Creek")
    page.locator("#room_type").select_option("Standard")
    page.locator("#child_room").select_option("1")
    page.get_by_role("button", name="Search").click()
    page.locator("#radiobutton_0").check()
    page.get_by_role("button", name="Continue").click()
    page.locator("#first_name").click()
    page.locator("#first_name").fill("Ali")
    page.locator("#last_name").click()
    page.locator("#last_name").fill("Khan")
    page.locator("#address").click()
    page.locator("#address").fill("asdsad")
    page.locator("#address").click()
    page.locator("#address").fill("asdsadS")
    page.locator("#address").click()
    page.locator("#address").click()
    page.locator("#address").click()
    page.locator("#address").fill("Street 1")
    page.locator("#cc_num").click()
    page.locator("#cc_num").fill("7861264565656565")
    page.locator("#cc_type").select_option("AMEX")
    page.locator("#cc_exp_month").select_option("9")
    page.locator("#cc_exp_year").select_option("2029")
    page.locator("#cc_cvv").click()
    page.locator("#cc_cvv").fill("7865")
    page.get_by_role("button", name="Book Now").click()
    expect(page.locator("#process_span")).to_contain_text("Please wait! We are processing your Hotel Booking...")
    page.get_by_role("button", name="Search Hotel").click()
    page.get_by_role("link", name="Logout").click()
    page.get_by_role("link", name="Click here to login again").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
