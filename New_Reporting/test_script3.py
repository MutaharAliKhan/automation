import re
import pytest
import allure
from playwright.sync_api import Page




@pytest.mark.parametrize("username, password", [
    ("standard_user", "secret_sauce"),
    ("standard_user", "secret_sauce"),
    ("standard_user", "secret_sauce"),
])
@allure.feature('test_example')
@allure.story('test_example1')
@allure.title('test_example2')
def test_example(page: Page, username: str, password: str) -> None:
    page.goto("https://www.saucedemo.com/v1/")
    page.locator("[data-test=\"username\"]").click()
    page.locator("[data-test=\"username\"]").fill(username)
    page.locator("[data-test=\"password\"]").click()
    page.locator("[data-test=\"password\"]").fill(password)
    page.get_by_role("button", name="LOGIN").click()
    page.locator("div").filter(has_text=re.compile(r"^\$29\.99ADD TO CART$")).get_by_role("button").click()
    page.get_by_role("button", name="ADD TO CART").nth(1).click()
    page.locator("div").filter(has_text=re.compile(r"^\$9\.99ADD TO CART$")).get_by_role("button").click()
    page.get_by_role("button", name="Open Menu").click()
    page.get_by_role("link", name="Logout").click()




