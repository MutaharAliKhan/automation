import pandas as pd
import random
import socket
from database.Queries import *
from database.database_connection import *
from utils.utils import *

test_data = read_json(r"D:\MyRecentProjects\Data_Utility\database\test_data.json")
current_branch_code = test_data['branch_code']
username = test_data['username']
authorizer = test_data['authorizer']
password = test_data['password']



def update_system_ip():
    current_system_ip = get_system_ip()
    execute_query(int(current_branch_code), Queries.update_user_system_ip,
                  values=(current_system_ip, current_branch_code))


def get_system_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        print("Error:", e)
        return None


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


