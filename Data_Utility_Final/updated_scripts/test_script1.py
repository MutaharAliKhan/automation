import pytest
import random
import pandas as pd
import allure
from database.database_operations import *
from playwright.sync_api import Page, expect




test_data = read_json(r'D:\MyRecentProjects\Data_Utility\database\test_data.json')


def read_values_from_csv():
    df = pd.read_csv(r'D:\MyRecentProjects\Data_Utility\updated_scripts\test_script1.csv')
    return df.values.tolist()


csv_data = read_values_from_csv()


@allure.feature('test_script1')
@allure.story('test_script1')
@allure.title('test_script1')
@pytest.mark.parametrize('branch_code, branch_code1, branch_code2, branch_code3, branch_code4, username, username1, username2, username3, username4, username5, password, password1, password2, password3, password4, password5, submit, submit1, submit2, submit3, submit4, base_url', csv_data)
def test_run(page: Page, branch_code, branch_code1, branch_code2, branch_code3, branch_code4, username, username1, username2, username3, username4, username5, password, password1, password2, password3, password4, password5, submit, submit1, submit2, submit3, submit4, base_url) -> None:
    # Starting
    page.goto('https://www.99acres.com/login')
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    page.goto('https://www.99acres.com/login')
    # Lorem Ipsum is simply dummy text of the printing and typesetting industry.
    page.goto('https://www.99acres.com/login')
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
