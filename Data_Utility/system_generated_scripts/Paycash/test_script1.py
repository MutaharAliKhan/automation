import pytest
import random
import pandas as pd
import allure
from database.database_operations import *
from playwright.sync_api import Page, expect


def read_values_from_csv():
    df = pd.read_csv(r'D:\MyRecentProjects\Data_Utility\system_generated_scripts\Paycash\test_script1.csv')
    return df.values.tolist()


csv_data = read_values_from_csv()


@allure.feature('test_script1')
@allure.story('test_script1')
@allure.title('test_script1')
@pytest.mark.parametrize('branch_code, branch_code2, branch_code3, branch_code4, username, username2, submit, username3, password, password2, password3, password4, submit2, submit3, submit4, submit5, ForgotPassword, get_by_text, get_by_text2, get_by_text3, get_by_text4, get_by_text5, get_by_text6, get_by_text7, get_by_text8', csv_data)
def test_run(page: Page, branch_code, branch_code2, branch_code3, branch_code4, username, username2, submit, username3, password, password2, password3, password4, submit2, submit3, submit4, submit5, ForgotPassword, get_by_text, get_by_text2, get_by_text3, get_by_text4, get_by_text5, get_by_text6, get_by_text7, get_by_text8, base_url) -> None:
    """
    Script Name: <Your Script Name>
    Description: <Paycash brief description of what the script does>
    
    Author: <Your Name>
    Created Date: <Date when the script was created>
    Last Modified Date: <Date of the last modification>
    Version: <Version of the script, e.g., 1.0, 1.1>
    Reviewed By: <Name of the person who reviewed the script, if applicable>
    Review Date: <Date when the script was reviewed, if applicable>
    Tested By: <Name of the person/team who tested the script, if applicable>
    Test Date: <Date when the script was tested, if applicable>
    
    Dependencies: <List any dependencies required by the script, e.g., libraries, external files>
    Execution: <Instructions on how to execute the script, if necessary>
    
    Change Log:
    - <Date>: <Description of changes made>
    
    """
    
    # page.goto
    page.goto(base_url)
    page.goto(base_url)
    page.goto(base_url)
    page.goto(base_url)
    '''ABC'''
    # random
    page.locator('#branch_code').fill(str(random.randint(1, 5000)))
    page.get_by_label('#branch_code').fill(str(random.randint(1, 3000)))
    page.get_by_placeholder('#branch_code').fill(str(random.randint(1, 4000)))
    page.get_by_label('#branch_code').fill(str(random.randint(1, 8000)))
    page.fill("input[type='submit']", str(random.randint(1, 1000)))
    
    '''ABC'''
    page.locator('#branch_code').fill(str(random.randint(1, 5000)))
    page.get_by_label('#branch_code').fill(str(random.randint(1, 3000)))
    page.get_by_placeholder('#branch_code').fill(str(random.randint(1, 4000)))
    page.get_by_label('#branch_code').fill(str(random.randint(1, 8000)))
    page.fill("input[type='submit']", str(random.randint(1, 1000)))
    
    #  page.locator
    page.locator('#branch_code').fill(str(branch_code))
    page.locator('#branch_code').fill(str(branch_code2))
    page.locator('#branch_code').fill(str(branch_code3))
    page.locator('#branch_code').fill(str(branch_code4))
    '''ABC'''
    # page.get_by_label
    page.get_by_label('data-e2e-username').fill(str(username))
    page.get_by_label('data-e2e-username').fill(str(username2))
    page.get_by_label("input[type='submit']").fill(str(submit))
    page.get_by_label('data-e2e-username').fill(str(username3))
    
    '''ABC'''
    page.get_by_label('data-e2e-username').fill(str(password))
    page.get_by_label('data-e2e-username').fill(str(password2))
    page.get_by_label("input[type='submit']").fill(str(password3))
    page.get_by_label('data-e2e-username').fill(str(password4))
    
    #  page.get_by_placeholder
    page.get_by_placeholder('data-test-password').fill(str(submit2))
    page.get_by_placeholder('data-test-password').fill(str(submit3))
    page.get_by_placeholder('data-test-password').fill(str(submit4))
    page.get_by_placeholder('data-test-password').fill(str(submit5))
    '''ABC'''
    #  page.fill
    page.fill("input[type='submit']", str(ForgotPassword))
    page.fill("input[type='submit']", str(get_by_text))
    page.fill("input[type='submit']", str(get_by_text2))
    page.fill("input[type='submit']", str(get_by_text3))
    
    '''ABC'''
    page.fill("input[type='submit']", str(get_by_text4))
    page.fill("input[type='submit']", str(get_by_text5))
    page.fill("input[type='submit']", str(get_by_text6))
    page.fill("input[type='submit']", str(get_by_text7))
    
    # page.get_by_text
    page.get_by_text('Forgot Password?').press()
    page.get_by_text('Forgot Password?').click()
    page.get_by_text('Subscribe').check()
    page.get_by_text('Subscribe').uncheck()
    page.get_by_text('Input field').press('Enter')
    page.get_by_text('Hover me').hover()
    page.get_by_text('Select an option').select_option('Option 1')
    page.get_by_text('Forgot Password?').fill(str(get_by_text8))
    page.wait_for_timeout(3000)
    expect(page.locator('.class')).to_have_text('fine')
    page.locator('.class').press()
    expect(page.locator('.class')).to_have_text('fine')
    expect(page.locator('.class')).to_have_text('fine')
    expect(page.locator('.class')).to_have_text('fine')
    expect(page.locator('.class')).to_have_text('fine')
    expect(page.locator('.class')).to_have_text('fine')