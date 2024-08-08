import random
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) ->None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    # Starting
    page.goto("https://www.99acres.com/login")
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    page.goto("https://www.99acres.com/login")
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    page.goto("https://www.99acres.com/login")
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    page.locator('#branch_code').fill(random.randint(1, 1000))
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill(random.randint(1, 1000))
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    '''11111111111111111111111111111111111111111111111111111111111111'''
    '''222222222222222222222222222222222222222222222222222222222222222'''
    page.get_by_label('data-e2e-username').fill('TESTING')
    page.get_by_label('data-e2e-username').fill('TESTING')
    page.get_by_label('data-e2e-username').fill('TESTING')
    page.get_by_label('data-e2e-username').fill('TESTING')
    page.get_by_label('data-e2e-username').fill('TESTING')
    page.get_by_label('data-e2e-username').fill('TESTING')
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    '''333333333333333333333333333333333333333333333333333333333333333333333333'''
    '''333333333333333333333333333333333333333333333333333333333333333333333333'''
    page.get_by_placeholder('data-test-password').fill('TESTING1')
    page.get_by_placeholder('data-test-password').fill('TESTING1')
    page.get_by_placeholder('data-test-password').fill('TESTING1')
    page.get_by_placeholder('data-test-password').fill('TESTING1')
    page.get_by_placeholder('data-test-password').fill('TESTING1')
    page.get_by_placeholder('data-test-password').fill('TESTING1')
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    '''444444444444444444444444444444444444444444444444444444444444444444444444444'''
    '''444444444444444444444444444444444444444444444444444444444444444444444444444'''
    page.fill("input[type='submit']", 'fine')
    page.fill("input[type='submit']", 'fine')
    page.fill("input[type='submit']", 'fine')
    page.fill("input[type='submit']", 'fine')
    page.fill("input[type='submit']", 'fine')
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    '''5555555555555555555555555555555555555555555555555555555555555555555555555555555'''
    '''5555555555555555555555555555555555555555555555555555555555555555555555555555555'''
    # Ending
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
