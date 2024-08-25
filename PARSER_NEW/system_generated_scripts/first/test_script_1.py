
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
    df = pd.read_csv(r"D:\MyRecentProjects\Data_Utility\system_generated_scripts\first\test_script_1.csv")
    return df.values.tolist()


csv_data = read_values_from_csv()


@allure.feature('script_1')
@allure.story('script_1')
@allure.title('script_1')
@pytest.mark.parametrize('get_text_value, firstname, password, username, submit, get_text_value1, get_fill_value1, get_text_value2, get_text_value3, button, button1, button2, button3, button4, button5, BUTTON, BUTTON1, BUTTON2, BUTTON3, BUTTON4, get_text_value4, get_text_value5, get_text_value6, get_text_value7, get_text_value8, get_text_value9, get_text_value10, submit1, submit2, button6, button7', csv_data)
def test_script_1(page: Page, get_text_value, firstname, password, username, submit, get_text_value1, get_fill_value1, get_text_value2, get_text_value3, button, button1, button2, button3, button4, button5, BUTTON, BUTTON1, BUTTON2, BUTTON3, BUTTON4, get_text_value4, get_text_value5, get_text_value6, get_text_value7, get_text_value8, get_text_value9, get_text_value10, submit1, submit2, button6, button7) -> None:
    update_system_ip()
    # comment'
    page.locator('#check').fill(str(random.randint(1, 100)))
    page.locator('#check').fill(str(random.randint(1, 100)))
    page.get_by_text(str(get_text_value)).fill(str(random.randint(1, 100)))
    page.get_by_label('data-e2e-firstname').fill(str(firstname))
    page.get_by_placeholder('data-test-password').fill(str(password))
    page.locator("#username").fill(str(username))
    page.fill("input[type='submit']", str(submit))
    page.get_by_text(str(get_text_value1)).fill(str(get_fill_value1))
    page.get_by_text(str(get_text_value2)).click()
    page.get_by_text(str(get_text_value3)).press("Enter")
    page.locator('#button').filter(has_text=str(button))
    page.locator('#button').filter(has_text=str(button1))
    page.locator('#button').filter(has_text=str(button2))
    page.locator('#button').filter(has_text=str(button3))
    page.locator('#button').filter(has_text=str(button4))
    page.locator('#button').filter(has_text=str(button5))
    page.get_by_role('BUTTON', name='Welcome').filter(has_text=str(BUTTON))
    page.get_by_role('BUTTON', name='Welcome').filter(has_text=str(BUTTON1))
    page.get_by_role('BUTTON', name='Welcome').filter(has_text=str(BUTTON2))
    page.get_by_role('BUTTON', name='Welcome').filter(has_text=str(BUTTON3))
    page.get_by_role('BUTTON', name='Welcome').filter(has_text=str(BUTTON4))
    page.get_by_text(str(get_text_value4)).click()
    page.get_by_text(str(get_text_value5)).click()
    page.get_by_text(str(get_text_value6)).click()
    page.get_by_text(str(get_text_value7)).click()
    page.get_by_text(str(get_text_value8)).click()
    page.get_by_text(str(get_text_value9)).click()
    page.get_by_text(str(get_text_value10)).click()
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
    page.get_by_role('submit', name='Welcome').fill(str(submit1))
    page.get_by_role('submit', name='Welcome').fill(str(submit2))
    page.get_by_role('button', name='Ok').fill(str(button6))
    page.get_by_role('button', name='Fine').fill(str(button7))
    # ---------------------
