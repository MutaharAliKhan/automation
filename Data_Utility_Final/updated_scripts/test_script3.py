import pytest
import random
import pandas as pd
import allure
from database.database_operations import *
from playwright.sync_api import Page, expect




test_data = read_json(r'D:\MyRecentProjects\Data_Utility\database\test_data.json')


def read_values_from_csv():
    df = pd.read_csv(r'D:\MyRecentProjects\Data_Utility\updated_scripts\test_script3.csv')
    return df.values.tolist()


csv_data = read_values_from_csv()


@allure.feature('test_script3')
@allure.story('test_script3')
@allure.title('test_script3')
@pytest.mark.parametrize('branch_code, branch_code1, branch_code2, branch_code3, branch_code4, branch_code5, branch_code6, branch_code7, branch_code8, branch_code9, branch_code10, branch_code11, branch_code12, branch_code13, branch_code14, branch_code15, branch_code16, branch_code17, base_url', csv_data)
def test_run(page: Page, branch_code, branch_code1, branch_code2, branch_code3, branch_code4, branch_code5, branch_code6, branch_code7, branch_code8, branch_code9, branch_code10, branch_code11, branch_code12, branch_code13, branch_code14, branch_code15, branch_code16, branch_code17, base_url) -> None:
    page.goto('https://www.99acres.com/login')
    page.goto('https://www.99acres.com/login')
    page.goto('https://www.99acres.com/login')
    page.goto('https://www.99acres.com/login')
    page.goto('https://www.99acres.com/login')
    page.goto('https://www.99acres.com/login')
    page.goto('https://www.99acres.com/login')
    page.goto('https://www.99acres.com/login')
    page.goto('https://www.99acres.com/login')
    page.goto('https://www.99acres.com/login')
    page.goto('https://www.99acres.com/login')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill('1026')
    page.locator('#branch_code').fill(random.randint(1, 1000))
    page.locator('#branch_code').fill(random.randint(1, 1000))
    page.locator('#branch_code').fill(random.randint(1, 1000))
    page.locator('#branch_code').fill(random.randint(1, 1000))
    page.locator('#branch_code').fill(random.randint(1, 1000))
    page.locator('#branch_code').fill(random.randint(1, 1000))
    page.locator('#branch_code').fill(random.randint(1, 1000))
    page.locator('#branch_code').fill(random.randint(1, 1000))
    page.locator('#branch_code').fill(random.randint(1, 1000))
    page.locator('#branch_code').fill(random.randint(1, 1000))
