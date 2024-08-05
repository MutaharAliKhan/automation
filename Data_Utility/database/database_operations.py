import pandas as pd


#
# def test_script1_data():
#     data = {
#         'branch_code': '1026',
#         'username': 'TESTING2',
#         'password': 'TESTING2',
#         }
#     return data
#
#
# def test_script2_data():
#     data = {
#         'branch_code': '1026',
#         'username': 'TESTING2',
#         'password': 'TESTING2',
#         }
#     return data


def test_script1_data():
    data = [
        {'branch_code': '5001', 'username': 'TESTING2', 'password': 'TESTING2'},
        {'branch_code': '5002', 'username': 'TESTING3', 'password': 'TESTING3'},
        {'branch_code': '5003', 'username': 'TESTING4', 'password': 'TESTING4'},
        {'branch_code': '5004', 'username': 'TESTING5', 'password': 'TESTING5'},
        {'branch_code': '5005', 'username': 'TESTING6', 'password': 'TESTING6'},
        {'branch_code': '5006', 'username': 'TESTING7', 'password': 'TESTING7'},
        {'branch_code': '5007', 'username': 'TESTING8', 'password': 'TESTING8'},
        {'branch_code': '5001', 'username': 'TESTING2', 'password': 'TESTING2'},  # Duplicate
        {'branch_code': '5002', 'username': 'TESTING3', 'password': 'TESTING3'},  # Duplicate
        {'branch_code': '5008', 'username': 'TESTING9', 'password': 'TESTING9'},
        {'branch_code': '5009', 'username': 'TESTING10', 'password': 'TESTING10'},
    ]
    return pd.DataFrame(data)


def test_script2_data():
    data = [
        {'branch_code': '5004', 'username': 'TESTING5', 'password': 'TESTING5'},
        {'branch_code': '5005', 'username': 'TESTING6', 'password': 'TESTING6'},
        {'branch_code': '5006', 'username': 'TESTING7', 'password': 'TESTING7'},
        {'branch_code': '5007', 'username': 'TESTING8', 'password': 'TESTING8'},
        {'branch_code': '5008', 'username': 'TESTING9', 'password': 'TESTING9'},
        {'branch_code': '5009', 'username': 'TESTING10', 'password': 'TESTING10'},
        {'branch_code': '5010', 'username': 'TESTING11', 'password': 'TESTING11'},
        {'branch_code': '5011', 'username': 'TESTING12', 'password': 'TESTING12'},
        {'branch_code': '5012', 'username': 'TESTING13', 'password': 'TESTING13'},
        {'branch_code': '5004', 'username': 'TESTING5', 'password': 'TESTING5'},  # Duplicate
        {'branch_code': '5005', 'username': 'TESTING6', 'password': 'TESTING6'},  # Duplicate
    ]
    return pd.DataFrame(data)
