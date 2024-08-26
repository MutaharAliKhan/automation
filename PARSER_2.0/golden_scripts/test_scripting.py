"""Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's
standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a
type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting,
remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem
Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem
Ipsum."""

import random
import re
from playwright.sync_api import Playwright, sync_playwright, expect
from conftest import PROJECT_ROOT


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # comment'
    page.goto('https://demoqa.com/text-box')
    page.locator('#check').fill(str(random.randint(1, 100)))
    page.locator('#check').fill(random.randint(1, 100))
    page.get_by_text('sadsadasdsadasdasdasffdsf').fill(str(random.randint(1, 100)))

    # comment'
    page.get_by_label('data-e2e-firstname').fill('test1')
    page.get_by_placeholder('data-test-password').fill('test2')
    page.locator("#username").fill('test3')
    page.fill("input[type='submit']", 'test4')
    page.get_by_text('wine').fill('fine')
    page.get_by_text('testing1').click()
    page.get_by_text('testing2').press("Enter")

    # comment'
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
    # comment
    # comment
    # comment
    # comment
    # comment
    # comment
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
    # comment
    # comment
    # comment
    # comment
    # comment
    # comment
    # comment
    # comment
    # comment
    # comment
    # comment
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    expect(page.get_by_text('Welcome')).to_be_visible()
    # comment'
    expect(page.get_by_text('Welcome')).fill('Cancel')
    # comment'
    page.get_by_role('submit', name='Welcome').fill('Ali_1')
    page.get_by_role('submit', name='Welcome').fill('Ali_2')
    page.get_by_role('button', name='Ok').fill('Ali_3')
    page.get_by_role('button', name='Fine').fill('Ali_4')

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
