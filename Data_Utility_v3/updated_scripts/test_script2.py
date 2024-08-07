import pytest
import pandas as pd
import allure
from database.database_operations import *
from playwright.sync_api import Page, expect




test_data = read_json(r'D:\MyRecentProjects\Data_Utility\database\test_data.json')


def read_values_from_csv():
    df = pd.read_csv(r'D:\MyRecentProjects\Data_Utility\updated_scripts\test_script2.csv')
    return df.values.tolist()


csv_data = read_values_from_csv()


@allure.feature('test_script2')
@allure.story('test_script2')
@allure.title('test_script2')
@pytest.mark.parametrize('customer_number, customer_number1, account_, account_1, run_number, run_number1, check_digit, check_digit1, account_balance_x, account_balance_x1, base_url', csv_data)
def test_run(page: Page, customer_number, customer_number1, account_, account_1, run_number, run_number1, check_digit, check_digit1, account_balance_x, account_balance_x1, base_url) -> None:
    page.get_by_label('customer_number').fill('12345')
    page.get_by_label('customer_number').fill('12345')
    page.get_by_label('account_type').fill('Savings')
    page.get_by_label('account_type').fill('Savings')
    page.get_by_label('run_number').fill('001')
    page.get_by_label('run_number').fill('001')
    page.get_by_label('check_digit').fill('9')
    page.get_by_label('check_digit').fill('9')
    page.get_by_label('account_balance_x').fill('500.00')
    page.get_by_label('account_balance_x').fill('500.00')
