import pytest
import pandas as pd
import allure
from playwright.sync_api import Page, expect


def read_values_from_csv():
    df = pd.read_csv(
        'D:\\MyRecentProjects\\Data_Utility\\updated_scripts\\test_script1.csv'
        )
    return df.values.tolist()


csv_data = read_values_from_csv()


@allure.feature('test_script1')
@allure.story('test_script1')
@allure.title('test_script1')
@pytest.mark.parametrize('branch_code, username, password', csv_data)
def test_run(page: Page, branch_code, username, password) ->None:
    page.get_by_label('branch_code').fill(str(branch_code))
    page.get_by_label('username').fill(str(username))
    page.get_by_label('password').fill(str(password))
