
import pytest
import random
import pandas as pd
import allure
from database.database_operations import *
from playwright.sync_api import Page, expect
from utils.pre_req_test import pre_req_user_setup
from utils.utils import base_url


def read_values_from_csv():
    pre_req_user_setup()
    df = pd.read_csv(r"D:\MyRecentProjects\Data_Utility\system_generated_scripts\test_sauce_demo.csv")
    return df.values.tolist()


csv_data = read_values_from_csv()


@allure.feature('sauce_demo')
@allure.story('sauce_demo')
@allure.title('sauce_demo')
@pytest.mark.parametrize('username, password, firstName, lastName, postalCode', csv_data)
def test_sauce_demo(page: Page, username, password, firstName, lastName, postalCode) -> None:
    update_system_ip()
    page.locator("body").click()
    page.goto(base_url)
    page.locator("[data-test=\"username\"]").click()
    page.locator("[data-test=\"username\"]").fill(str(username))
    page.locator("[data-test=\"password\"]").click()
    page.locator("[data-test=\"password\"]").fill(str(password))
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
    page.locator("[data-test=\"firstName\"]").fill(str(firstName))
    page.locator("[data-test=\"firstName\"]").press("Tab")
    page.locator("[data-test=\"lastName\"]").fill(str(lastName))
    page.locator("[data-test=\"lastName\"]").press("Tab")
    page.locator("[data-test=\"postalCode\"]").fill(str(postalCode))
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
