import pandas as pd
import random
import socket
from database.Queries import *
from database.database_connection import *
from conftest import *
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





def sauce_demo_data():

    result = execute_query(int(current_branch_code), Queries.fetch_customer,
                           values=(current_branch_code, "586", "81"))

    if isinstance(result, list):
        data = [{
            'username': 'standard_user',
            'password': 'secret_sauce',
            'firstName': 'Ali',
            'lastName': 'Khan',
            'postalCode': '7500'
        } for row in result]
        return pd.DataFrame(data)




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




def script_10_data():

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




def script_4_data():

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




def script_5_data():

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




def script_6_data():

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




def script_7_data():

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




def script_8_data():

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




def script_9_data():

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

