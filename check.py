import re
import logging

def method_exists(file_path, method_name):
    """
    Check if a method exists in the given file.
    Method should not be commented out.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Remove commented-out lines to avoid false positives
        uncommented_content = re.sub(r'#.*', '', content)
        
        pattern = rf'\bdef {method_name}\('
        if re.search(pattern, uncommented_content):
            return True
    except Exception as e:
        logging.error(f"Error checking method existence in file {file_path}: {e}")
    
    return False

def add_method(file_path, method_name):
    """
    Add a new method to the given file if it does not already exist.
    """
    base_name = method_name.replace('_data', '')
    method_code = f"""
def {method_name.replace('test_', '')}(current_branch_code: int, currency_code: str, account_type: str):
    result = execute_query(current_branch_code, Queries.fetch_customer,
                           values=(current_branch_code, currency_code, account_type))

    data = {{
        '''Get Data From Database''': result
    }}
    write_to_csv(data, '{base_name}')\n
"""

    try:
        with open(file_path, 'r') as file:
            content = file.read()

        if method_exists(file_path, method_name):
            logging.info(f"Method '{method_name}' already exists in {file_path}.")
            return

        # Check if imports are needed
        imports_needed = """import pandas as pd
from database.Queries import *
from database.database_connection import *"""
        
        if imports_needed not in content:
            with open(file_path, 'r+') as file:
                existing_content = file.read()
                file.seek(0, 0)
                # Write imports at the top, if not already present
                file.write(f"{imports_needed}\n\n{existing_content}")

        with open(file_path, 'a') as file:
            file.write(method_code)

        logging.info(f"Added method '{method_name}' to {file_path}")
    except Exception as e:
        logging.error(f"Error adding method '{method_name}' to {file_path}: {e}")

