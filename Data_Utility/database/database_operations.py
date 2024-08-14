import pandas as pd
import random
import socket
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


def test_script1_data():
    update_system_ip()
    result = [
        {'branch_code': '0012', 'customer_id': '1234', 'name': 'John Doe2'},
    ]

    if isinstance(result, list):
        data = [{'branch_code': row['branch_code'],
                 'customer_id': row['customer_id'],
                 'name': row['name'],
                 } for row in result]
        return pd.DataFrame(data)


# def test_script2_data():
#     data = [
#         {'branch_code': test_data['branch_code'],
#          'username': test_data['username'],
#          'password': test_data['password'],
#          'narration': generate_random_number(1, 1000),
#          'payslip': generate_random_number(1, 1000),
#          'cnic': generate_random_number(1, 1000),
#          'amount': generate_random_number(1, 1000),
#          'receipt': generate_random_number(1, 1000)},
#         {'branch_code': test_data['branch_code'],
#          'username': test_data['username'],
#          'password': test_data['password'],
#          'narration': generate_random_number(1, 1000),
#          'payslip': generate_random_number(1, 1000),
#          'cnic': generate_random_number(1, 1000),
#          'amount': generate_random_number(1, 1000),
#          'receipt': generate_random_number(1, 1000)},
#         {'branch_code': test_data['branch_code'],
#          'username': test_data['username'],
#          'password': test_data['password'],
#          'narration': generate_random_number(1, 1000),
#          'payslip': generate_random_number(1, 1000),
#          'cnic': generate_random_number(1, 1000),
#          'amount': generate_random_number(1, 1000),
#          'receipt': generate_random_number(1, 1000)},
#     ]
#     return pd.DataFrame(data)


def test_script4_data():
    result = execute_query(int(current_branch_code), Queries.fetch_customer,
                           values=(current_branch_code, "586", "81"))

    if isinstance(result, list):
        update_system_ip()
        data = [{'"test"'} for row in result]
        return pd.DataFrame(data)
