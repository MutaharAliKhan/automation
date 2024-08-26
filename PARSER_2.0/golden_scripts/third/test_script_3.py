import random
import re
from playwright.sync_api import Playwright, sync_playwright, expect
from conftest import PROJECT_ROOT


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # comment'
    page.locator('#check').fill(str(random.randint(1, 100)))
    page.locator('#check').fill(random.randint(1, 100))
    page.get_by_text('sadsadasdsadasdasdasffdsf').fill(str(random.randint(1, 100)))


    page.get_by_label('data-e2e-firstname').fill('test1')
    page.get_by_placeholder('data-test-password').fill('test2')
    page.locator("#username").fill('test3')
    page.fill("input[type='submit']", 'test4')
    page.get_by_text('wine').fill('fine')
    page.get_by_text('testing1').click()
    page.get_by_text('testing2').press("Enter")


    page.locator('#button').filter(has_text="dasdasd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.locator('#button').filter(has_text="asdasdsd")
    page.get_by_role('BUTTON', name='Welcome').filter(has_text="asdasdsd")
    page.get_by_role('BUTTON', name='Welcome').filter(has_text="asdasdsd")
    page.get_by_role('BUTTON', name='Welcome').filter(has_text="asdasdsd")
    page.get_by_role('BUTTON', name='Welcome').filter(has_text="asdasdsd")
    page.get_by_role('BUTTON', name='Welcome').filter(has_text="asdasdsd")
    page.get_by_text('Submit').click()
    page.get_by_text('Cancel').click()
    page.get_by_text('Cancel').click()
    page.get_by_text('Cancel').click()
    page.get_by_text('Cancel').click()
    page.get_by_text('Cancel').click()
    page.get_by_text('Cancel').click()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).fill('Cancel')
    page.get_by_role('submit', name='Welcome').fill('Ali_1')
    page.get_by_role('submit', name='Welcome').fill('Ali_2')
    page.get_by_role('button', name='Ok').fill('Ali_3')
    page.get_by_role('button', name='Fine').fill('Ali_4')

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
