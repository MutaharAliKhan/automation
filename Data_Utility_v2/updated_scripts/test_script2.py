import pytest
import pandas as pd
import allure
from database.database_operations import *
from playwright.sync_api import Page, expect
test_data = read_json(
    'D:\\MyRecentProjects\\Data_Utility\\database\\test_data.json')


def read_values_from_csv():
    script2_data(test_data['branch_code'])
    df = pd.read_csv(
        'D:\\MyRecentProjects\\Data_Utility\\updated_scripts\\test_script2.csv'
        )
    return df.values.tolist()


csv_data = read_values_from_csv()


@allure.feature('test_script2')
@allure.story('test_script2')
@allure.title('test_script2')
@pytest.mark.parametrize(
    'customer_number, account_type, run_number, check_digit, account_balance_x'
    , csv_data)
def test_run(page: Page, customer_number, account_type, run_number,
    check_digit, account_balance_x) ->None:
    page.get_by_label('customer_number').fill(str(customer_number))
    page.get_by_label('account_type').fill(str(account_type))
    page.get_by_label('run_number').fill(str(run_number))
    page.get_by_label('check_digit').fill(str(check_digit))
    page.get_by_label('account_balance_x').fill(str(account_balance_x))
