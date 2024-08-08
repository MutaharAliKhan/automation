import pandas as pd
import random
from database.Queries import *
from database.database_connection import *
test_data = read_json(r"D:\MyRecentProjects\Data_Utility\database\test_data.json")

def test_script4_data():
    data = [
        {'branch_code': test_data['branch_code'], 'username': test_data['username'], 'Account': random.randint(1, 1000)},
        {'branch_code': test_data['branch_code'], 'username': test_data['username'], 'Account': random.randint(1, 1000)},
        {'branch_code': test_data['branch_code'], 'username': test_data['username'], 'Account': random.randint(1, 1000)},
        {'branch_code': test_data['branch_code'], 'username': test_data['username'], 'Account': random.randint(1, 1000)},
        {'branch_code': test_data['branch_code'], 'username': test_data['username'], 'Account': random.randint(1, 1000)},
        {'branch_code': test_data['branch_code'], 'username': test_data['username'], 'Account': random.randint(1, 1000)},
    ]
    return pd.DataFrame(data)
