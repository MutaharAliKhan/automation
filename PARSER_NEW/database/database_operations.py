import pandas as pd
from database.Queries import *
from database.database_connection import *
from utils.utils import *


test_data = read_json(get_file_location('test_data.json'))
current_branch_code = test_data['branch_code']
username = test_data['username']
authorizer = test_data['authorizer']
password = test_data['password']


def update_system_ip():
    current_system_ip = get_system_ip()
    execute_query(int(current_branch_code), Queries.update_user_system_ip,
                  values=(current_system_ip, current_branch_code))





def scripting_data():

    result = execute_query(int(current_branch_code), Queries.fetch_customer,
                           values=(current_branch_code, "586", "81"))

    if isinstance(result, list):
        data = [{
            'get_text_value': current_branch_code,
            'firstname': 'test1',
            'password': 'test2',
            'username': 'test3',
            'submit': 'test4',
            'get_text_value1': 'wine',
            'get_fill_value1': 'fine',
            'get_text_value2': 'testing1',
            'get_text_value3': 'testing2',
            'button': 'dasdasd',
            'button1': 'asdasdsd',
            'button2': 'asdasdsd',
            'button3': 'asdasdsd',
            'button4': 'asdasdsd',
            'button5': 'asdasdsd',
            'BUTTON': 'asdasdsd',
            'BUTTON1': 'asdasdsd',
            'BUTTON2': 'asdasdsd',
            'BUTTON3': 'asdasdsd',
            'BUTTON4': 'asdasdsd',
            'get_text_value4': 'Submit',
            'get_text_value5': 'Cancel',
            'get_text_value6': 'Cancel',
            'get_text_value7': 'Cancel',
            'get_text_value8': 'Cancel',
            'get_text_value9': 'Cancel',
            'get_text_value10': 'Cancel',
            'submit1': 'Ali_1',
            'submit2': 'Ali_2',
            'button6': 'Ali_3',
            'button7': 'Ali_4'
                 } for row in result]
        return pd.DataFrame(data)




def script_1_data():

    result = execute_query(int(current_branch_code), Queries.fetch_customer,
                           values=(current_branch_code, "586", "81"))

    if isinstance(result, list):
        data = [{
            'get_text_value': current_branch_code,
            'firstname': 'test1',
            'password': 'test2',
            'username': 'test3',
            'submit': 'test4',
            'get_text_value1': 'wine',
            'get_fill_value1': 'fine',
            'get_text_value2': 'testing1',
            'get_text_value3': 'testing2',
            'button': 'dasdasd',
            'button1': 'asdasdsd',
            'button2': 'asdasdsd',
            'button3': 'asdasdsd',
            'button4': 'asdasdsd',
            'button5': 'asdasdsd',
            'BUTTON': 'asdasdsd',
            'BUTTON1': 'asdasdsd',
            'BUTTON2': 'asdasdsd',
            'BUTTON3': 'asdasdsd',
            'BUTTON4': 'asdasdsd',
            'get_text_value4': 'Submit',
            'get_text_value5': 'Cancel',
            'get_text_value6': 'Cancel',
            'get_text_value7': 'Cancel',
            'get_text_value8': 'Cancel',
            'get_text_value9': 'Cancel',
            'get_text_value10': 'Cancel',
            'submit1': 'Ali_1',
            'submit2': 'Ali_2',
            'button6': 'Ali_3',
            'button7': 'Ali_4'
                 } for row in result]
        return pd.DataFrame(data)




def script_2_data():

    result = execute_query(int(current_branch_code), Queries.fetch_customer,
                           values=(current_branch_code, "586", "81"))

    if isinstance(result, list):
        data = [{
            'get_text_value': current_branch_code,
            'firstname': 'test1',
            'password': 'test2',
            'username': 'test3',
            'submit': 'test4',
            'get_text_value1': 'wine',
            'get_fill_value1': 'fine',
            'get_text_value2': 'testing1',
            'get_text_value3': 'testing2',
            'button': 'dasdasd',
            'button1': 'asdasdsd',
            'button2': 'asdasdsd',
            'button3': 'asdasdsd',
            'button4': 'asdasdsd',
            'button5': 'asdasdsd',
            'BUTTON': 'asdasdsd',
            'BUTTON1': 'asdasdsd',
            'BUTTON2': 'asdasdsd',
            'BUTTON3': 'asdasdsd',
            'BUTTON4': 'asdasdsd',
            'get_text_value4': 'Submit',
            'get_text_value5': 'Cancel',
            'get_text_value6': 'Cancel',
            'get_text_value7': 'Cancel',
            'get_text_value8': 'Cancel',
            'get_text_value9': 'Cancel',
            'get_text_value10': 'Cancel',
            'submit1': 'Ali_1',
            'submit2': 'Ali_2',
            'button6': 'Ali_3',
            'button7': 'Ali_4'
                 } for row in result]
        return pd.DataFrame(data)




def script_3_data():

    result = execute_query(int(current_branch_code), Queries.fetch_customer,
                           values=(current_branch_code, "586", "81"))

    if isinstance(result, list):
        data = [{
            'get_text_value': current_branch_code,
            'firstname': 'test1',
            'password': 'test2',
            'username': 'test3',
            'submit': 'test4',
            'get_text_value1': 'wine',
            'get_fill_value1': 'fine',
            'get_text_value2': 'testing1',
            'get_text_value3': 'testing2',
            'button': 'dasdasd',
            'button1': 'asdasdsd',
            'button2': 'asdasdsd',
            'button3': 'asdasdsd',
            'button4': 'asdasdsd',
            'button5': 'asdasdsd',
            'BUTTON': 'asdasdsd',
            'BUTTON1': 'asdasdsd',
            'BUTTON2': 'asdasdsd',
            'BUTTON3': 'asdasdsd',
            'BUTTON4': 'asdasdsd',
            'get_text_value4': 'Submit',
            'get_text_value5': 'Cancel',
            'get_text_value6': 'Cancel',
            'get_text_value7': 'Cancel',
            'get_text_value8': 'Cancel',
            'get_text_value9': 'Cancel',
            'get_text_value10': 'Cancel',
            'submit1': 'Ali_1',
            'submit2': 'Ali_2',
            'button6': 'Ali_3',
            'button7': 'Ali_4'
                 } for row in result]
        return pd.DataFrame(data)




def script1_data():

    result = execute_query(int(current_branch_code), Queries.fetch_customer,
                           values=(current_branch_code, "586", "81"))

    if isinstance(result, list):
        data = [{
            'branch_code4': '1026',
            'branch_code5': '1026',
            'branch_code6': '1026',
            'branch_code7': '1026',
            'username': 'TESTING',
            'username1': 'TESTING',
            'submit1': 'TESTING',
            'username2': 'TESTING',
            'password': 'TESTING1',
            'password1': 'TESTING1',
            'password2': 'TESTING1',
            'password3': 'TESTING1',
            'submit2': 'fine',
            'submit3': 'fine',
            'submit4': 'fine',
            'submit5': 'fine',
            'get_text_value': current_branch_code,
            'get_text_value1': 'Forgot Password?',
            'get_text_value2': 'Subscribe',
            'get_text_value3': 'Subscribe',
            'get_text_value4': 'Input field',
            'get_text_value5': 'Hover me',
            'get_text_value6': 'Select an option',
            'get_text_value7': 'Forgot Password?',
            'get_fill_value': 'finally'
                 } for row in result]
        return pd.DataFrame(data)




def script2_data():

    result = execute_query(int(current_branch_code), Queries.fetch_customer,
                           values=(current_branch_code, "586", "81"))

    if isinstance(result, list):
        data = [{
            'branch_code': '1026',
            'username': 'VQATST1',
            'password': 'login11111',
            'narration': 'TESTING',
            'payslip': '12345',
            'cnic': '42201-1234567-1',
            'amount': '50000',
            'receipt': '54321'
                 } for row in result]
        return pd.DataFrame(data)




def script3_data():

    result = execute_query(int(current_branch_code), Queries.fetch_customer,
                           values=(current_branch_code, "586", "81"))

    if isinstance(result, list):
        data = [{

                 } for row in result]
        return pd.DataFrame(data)




def script4_data():

    result = execute_query(int(current_branch_code), Queries.fetch_customer,
                           values=(current_branch_code, "586", "81"))

    if isinstance(result, list):
        data = [{
            'username': 'Admin001',
            'password': 'N0C6LN',
            'first_name': 'Ali',
            'last_name': 'Khan',
            'address': 'asdsad',
            'address1': 'asdsadS',
            'address2': 'Street 1',
            'cc_num': '7861264565656565',
            'cc_cvv': '7865'
                 } for row in result]
        return pd.DataFrame(data)

