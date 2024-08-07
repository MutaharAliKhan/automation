from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) ->None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.get_by_label('customer_number').fill('12345')
    page.get_by_label('customer_number').fill('12345')
    page.get_by_label('account_type').fill('Savings')
    page.get_by_label('account_type').fill('Savings')
    page.get_by_label('run_number').fill('001')
    page.get_by_label('run_number').fill('001')
    page.get_by_label('check_digit').fill('9')
    page.get_by_label('check_digit').fill('9')
    page.get_by_label('account_balance_x').fill('500.00')
    page.get_by_label('account_balance_x').fill('500.00')
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
