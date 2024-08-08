import pytest
import random
import pandas as pd
import allure
from database.database_operations import *
from playwright.sync_api import Page, expect




test_data = read_json(r'D:\MyRecentProjects\Data_Utility\database\test_data.json')


def read_values_from_csv():
    df = pd.read_csv(r'D:\MyRecentProjects\Data_Utility\updated_scripts\test_script4.csv')
    return df.values.tolist()


csv_data = read_values_from_csv()


@allure.feature('test_script4')
@allure.story('test_script4')
@allure.title('test_script4')
@pytest.mark.parametrize('username, branch_code, Account, base_url', csv_data)
def test_sample_function(page: Page, username, branch_code, Account, base_url) -> None:
    # This is a sample script for demonstration
    page.locator('#username').fill('testuser')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill(random.randint(1, 1000))
    page.get_by_label('Account').fill('Savings')
    page.fill('#amount', random.randint(1, 1000))
    # Perform some other actions
    page.locator('#submit').click()
