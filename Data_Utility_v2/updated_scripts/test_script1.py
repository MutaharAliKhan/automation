import pytest
import pandas as pd
import allure
from conftest import base_url
from database.database_operations import *
from playwright.sync_api import Page, expect

test_data = read_json(
    'D:\\MyRecentProjects\\Data_Utility\\database\\test_data.json')


def read_values_from_csv():
    # script1_data(test_data['branch_code'])
    df = pd.read_csv(
        'D:\\MyRecentProjects\\Data_Utility\\updated_scripts\\test_script1.csv'
        )
    return df.values.tolist()


csv_data = read_values_from_csv()

@allure.feature('test_script1')
@allure.story('test_script1')
@allure.title('test_script1')
@pytest.mark.parametrize('branch_code, username, password', csv_data)
def test_run(page: Page, base_url, branch_code, username, password) -> None:
    print(base_url)
    # page.goto(url)
    # page.get_by_label('branch_code').fill(str(branch_code))
    # page.get_by_label('username').fill(str(username))
    # page.get_by_label('password').fill(str(password))