import pytest
import random
import pandas as pd
import allure
from database.database_operations import *
from playwright.sync_api import Page, expect



def read_values_from_csv():
    df = pd.read_csv(r'D:\MyRecentProjects\Data_Utility\system_generated_scripts\test_script4.csv')
    return df.values.tolist()


csv_data = read_values_from_csv()


@allure.feature('test_script4')
@allure.story('test_script4')
@allure.title('test_script4')
@pytest.mark.parametrize('username, password, first_name, last_name, address, address2, address3, cc_num, cc_cvv', csv_data)
def test_run(page: Page, username, password, first_name, last_name, address, address2, address3, cc_num, cc_cvv, base_url) -> None:
    page.goto(base_url)
    page.locator('#username').click()
    page.locator('#username').fill(str(username))
    page.locator('#password').click()
    page.locator('#password').fill(str(password))
    page.get_by_role('button', name='Login').click()
    page.locator('#location').select_option('Sydney')
    page.locator('#hotels').select_option('Hotel Creek')
    page.locator('#room_type').select_option('Standard')
    page.locator('#child_room').select_option('1')
    page.get_by_role('button', name='Search').click()
    page.locator('#radiobutton_0').check()
    page.get_by_role('button', name='Continue').click()
    page.locator('#first_name').click()
    page.locator('#first_name').fill(str(first_name))
    page.locator('#last_name').click()
    page.locator('#last_name').fill(str(last_name))
    page.locator('#address').click()
    page.locator('#address').fill(str(address))
    page.locator('#address').click()
    page.locator('#address').fill(str(address2))
    page.locator('#address').click()
    page.locator('#address').click()
    page.locator('#address').click()
    page.locator('#address').fill(str(address3))
    page.locator('#cc_num').click()
    page.locator('#cc_num').fill(str(cc_num))
    page.locator('#cc_type').select_option('AMEX')
    page.locator('#cc_exp_month').select_option('9')
    page.locator('#cc_exp_year').select_option('2029')
    page.locator('#cc_cvv').click()
    page.locator('#cc_cvv').fill(str(cc_cvv))
    page.get_by_role('button', name='Book Now').click()
    expect(page.locator('#process_span')).to_contain_text(
    'Please wait! We are processing your Hotel Booking...')
    page.get_by_role('button', name='Search Hotel').click()
    page.get_by_role('link', name='Logout').click()
    page.get_by_role('link', name='Click here to login again').click()

