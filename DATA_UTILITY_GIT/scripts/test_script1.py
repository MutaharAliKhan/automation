import pytest
import pandas as pd
import allure
from playwright.sync_api import Page


def read_values_from_csv():
    file_path = 'D:\\MyRecentProjects\\Data_Utility\\final_dump\\joined_data.csv'

    df = pd.read_csv(file_path, dtype=str)
    df_filtered = df[['customer_number', 'account_type', 'run_number', 'check_digit', 'branch_code']]
    return df_filtered.values.tolist()


csv_data = read_values_from_csv()


@allure.feature('test_script1')
@allure.story('test_script1')
@allure.title('test_script1')
@pytest.mark.parametrize(
    'customer_number,account_type,run_number,check_digit,branch_code',
    csv_data
)
def test_run(page: Page, customer_number, account_type, run_number, check_digit, branch_code) -> None:
    print(f'{customer_number} {account_type} {run_number} {check_digit} {branch_code}')
