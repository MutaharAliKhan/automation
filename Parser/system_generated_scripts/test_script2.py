import pytest
import random
import pandas as pd
import allure
from database.database_operations import *
from playwright.sync_api import Page, expect



def read_values_from_csv():
    df = pd.read_csv(r'D:\MyRecentProjects\Data_Utility\system_generated_scripts\test_script2.csv')
    return df.values.tolist()


csv_data = read_values_from_csv()


@allure.feature('test_script2')
@allure.story('test_script2')
@allure.title('test_script2')
@pytest.mark.parametrize('branch_code, username, password, narration, payslip, cnic, amount, receipt', csv_data)
def test_run(page: Page, branch_code, username, password, narration, payslip, cnic, amount, receipt, base_url) -> None:
    page.locator('branch_code').fill(str(branch_code))
    page.locator('username').fill(str(username))
    page.locator('password').fill(str(password))
    page.locator('narration').fill(str(narration))
    page.locator('payslip').fill(str(payslip))
    page.locator('cnic').fill(str(cnic))
    page.locator('amount').fill(str(amount))
    page.locator('receipt').fill(str(receipt))

