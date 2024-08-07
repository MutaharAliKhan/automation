import pandas as pd
from database.Queries import *
from database.database_connection import *

# def script1_data(current_branch_code: int, currency_code: str, account_type: str):
#     result = execute_query(current_branch_code, Queries.fetch_customer,
#                            values=(current_branch_code, currency_code, account_type))
#
#     data = {
#         '''Get Data From Database''': result
#     }
#     write_to_csv(data, 'test_script1')
#
#
# def script2_data(current_branch_code: int, currency_code: str, account_type: str):
#     result = execute_query(current_branch_code, Queries.fetch_customer,
#                            values=(current_branch_code, currency_code, account_type))
#
#     data = {
#         '''Get Data From Database''': result
#     }
#     write_to_csv(data, 'test_script2')


def script1_data(current_branch_code: int, currency_code: str, account_type: str):
    result = execute_query(current_branch_code, Queries.fetch_customer,
                           values=(current_branch_code, currency_code, account_type))

    data = {
        '''Get Data From Database''': result
    }
    write_to_csv(data, 'test_script1')


def script2_data(current_branch_code: int, currency_code: str, account_type: str):
    result = execute_query(current_branch_code, Queries.fetch_customer,
                           values=(current_branch_code, currency_code, account_type))

    data = {
        '''Get Data From Database''': result
    }
    write_to_csv(data, 'test_script2')

