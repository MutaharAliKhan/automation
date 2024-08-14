import os
import re
import csv
import ast
import astor
import logging
import pandas as pd
from utils.utils import get_folder_location, get_file_location


def parser(golden_script_dir, system_generated_scripts_dir):
    try:

        def setup_logging():
            log_dir = get_folder_location('logs')

            if log_dir is None:
                root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                log_dir = os.path.join(root_dir, 'logs')

                if not os.path.exists(log_dir):
                    os.makedirs(log_dir)

            log_file = os.path.join(log_dir, 'parser.log')

            logging.basicConfig(
                filename=log_file,
                level=logging.DEBUG,
                format='%(asctime)s - %(levelname)s - %(message)s'
            )
            return log_file

        def sanitize_name(name: str) -> str:
            name = (name.replace("data-e2e", "").replace("data-test", "")
                    .replace("input", "").replace("type", ""))
            name = re.sub(r'[^a-zA-Z0-9_]', '', name)
            return name

        def extract_string_literals(code_line):
            pattern = r"'(?:\\'|[^'])*'|\"(?:\\\"|[^\"])*\""
            matches = re.findall(pattern, code_line)
            strings = [re.sub(r"(^'|'$)|(^\"|\"$)", "", match).replace("\\'", "'").replace('\\"', '"') for match in
                       matches]
            return strings

        def extract_get_by_text(file):
            text_data = {}
            column_list = []
            column_count = {}
            try:
                with open(file, 'r') as f:
                    lines = f.readlines()

                for line_number, line in enumerate(lines, start=1):
                    if 'get_by_text' in line:
                        extracted_text = extract_string_literals(line)
                        if len(extracted_text) < 1:
                            continue

                        column_name = 'get_by_text'
                        value = sanitize_name(str(extracted_text[0]))

                        if column_name in column_count:
                            column_count[column_name] += 1
                            unique_column_name = f"{column_name}{column_count[column_name]}"
                        else:
                            column_count[column_name] = 1
                            unique_column_name = column_name

                        column_list.append(unique_column_name)
                        text_data[unique_column_name] = value

            except Exception as e:
                logging.error(f"Error extracting get_by_text data from {file}: {e}")

            return text_data

        def find_lines_with_fill(filepath):
            results = []
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                for line_number, line in enumerate(lines, start=1):
                    if 'fill' in line:
                        results.append((line_number, line.strip()))
            except Exception as e:
                logging.error(f"Error reading file {filepath}: {e}")
            return results

        def extract_fill_data(file):
            fill_data = {}
            column_list = []
            column_count = {}
            try:
                with open(file, 'r') as f:
                    file_content = f.read()

                result = find_lines_with_fill(file)
                text_data = extract_get_by_text(file)

                for line in result:
                    extracted_lines_strings = extract_string_literals(line[1])
                    if len(extracted_lines_strings) < 2:
                        continue

                    column_name = sanitize_name(str(extracted_lines_strings[0]))
                    if 'random.randint' in extracted_lines_strings[1]:
                        value = 'random'
                    else:
                        value = sanitize_name(str(extracted_lines_strings[1]))

                    if column_name in column_count:
                        column_count[column_name] += 1
                        unique_column_name = f"{column_name}{column_count[column_name]}"
                    else:
                        column_count[column_name] = 1
                        unique_column_name = column_name

                    column_list.append(unique_column_name)
                    fill_data[unique_column_name] = value

                fill_data.update(text_data)

            except Exception as e:
                logging.error(f"Error extracting fill data from {file}: {e}")
            return fill_data

        def save_data_to_csv(data, csv_path):
            try:
                df = pd.DataFrame(data)
                df.to_csv(csv_path, index=False)
                logging.info(f"Data saved to CSV at {csv_path}")
            except Exception as e:
                logging.error(f"Error saving data to CSV at {csv_path}: {e}")

        def extract_function_name(script_content):
            match = re.search(r'def (\w+)\(', script_content)
            return match.group(1) if match else 'run'

        def read_values_from_csv(csv_path):
            try:
                df = pd.read_csv(csv_path)
                values = df.values.tolist()
                return df.columns.tolist(), values
            except Exception as e:
                logging.error(f"Error reading values from CSV at {csv_path}: {e}")
                return [], []

        def method_exists(file_path, method_name):
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                uncommented_content = re.sub(r'#.*', '', content)
                pattern = rf'\bdef {method_name}\('
                return bool(re.search(pattern, uncommented_content))
            except Exception as e:
                logging.error(f"Error checking method existence in file {file_path}: {e}")
                return False

        def add_method(file_path, method_name):
            method_code = f"""
\ndef {method_name}():
    result = execute_query(int(current_branch_code), Queries.fetch_customer,
                           values=(current_branch_code, "586", "81"))

    if isinstance(result, list):
        update_system_ip()
        data = [{{'"test"'}} for row in result]
        return pd.DataFrame(data)\n
"""
            imports_needed = """import pandas as pd
import random
import socket
from database.Queries import *
from database.database_connection import *
from utils.utils import *

\ntest_data = read_json(get_file_location('test_data.json'))
current_branch_code = test_data['branch_code']
username = test_data['username']
authorizer = test_data['authorizer']
password = test_data['password']

\ndef update_system_ip():
    current_system_ip = get_system_ip()
    execute_query(int(current_branch_code), Queries.update_user_system_ip,
                  values=(current_system_ip, current_branch_code))
"""

            try:
                with open(file_path, 'r') as file:
                    content = file.read()

                if method_exists(file_path, method_name):
                    logging.info(f"Method '{method_name}' already exists in {file_path}.")
                    return

                normalized_content = re.sub(r'\s+', ' ', content.strip())
                normalized_imports_needed = re.sub(r'\s+', ' ', imports_needed.strip())

                if normalized_imports_needed not in normalized_content:
                    with open(file_path, 'r+') as file:
                        existing_content = file.read()
                        file.seek(0, 0)
                        file.write(f"{imports_needed}\n\n{existing_content}")

                with open(file_path, 'a') as file:
                    file.write(method_code)

                logging.info(f"Added method '{method_name}' to {file_path}")
            except Exception as e:
                logging.error(f"Error adding method '{method_name}' to {file_path}: {e}")

        def extract_comments(script_content):
            comments = {}
            lines = script_content.split('\n')

            in_multiline_comment = False
            multiline_comment_lines = []
            current_comment_start_index = None

            for index, line in enumerate(lines):
                stripped_line = line.strip()

                if stripped_line.startswith("'''") or stripped_line.startswith('"""'):
                    if in_multiline_comment:
                        multiline_comment_lines.append('    ' + stripped_line)
                        comments[current_comment_start_index] = '\n'.join(multiline_comment_lines)
                        in_multiline_comment = False
                        multiline_comment_lines = []
                    else:
                        in_multiline_comment = True
                        current_comment_start_index = index + 1
                        multiline_comment_lines.append('' + stripped_line)
                elif in_multiline_comment:
                    if stripped_line.endswith("'''") or stripped_line.endswith('"""'):
                        multiline_comment_lines.append('    ' + stripped_line)
                        comments[current_comment_start_index] = '\n'.join(multiline_comment_lines)
                        in_multiline_comment = False
                        multiline_comment_lines = []
                    else:
                        multiline_comment_lines.append('    ' + stripped_line)
                elif stripped_line.startswith('#'):
                    comments[index + 1] = '\n' + '    ' + stripped_line

            return comments

        def get_csv_headers(file_path):
            try:
                with open(file_path, mode='r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    headers = next(reader)
                return headers
            except Exception as e:
                print(f"Error reading CSV headers from {file_path}: {e}")
                return []

        def replace_arguments(file_path, headers):
            try:
                with open(file_path, 'r') as file:
                    code = file.read()

                fill_pattern = re.compile(r'\.fill\(([^)]+)\)', re.DOTALL)
                click_pattern = re.compile(r"page\.get_by_text\(([^)]+)\)", re.DOTALL)
                header_index = 0

                def replace_fill(match):
                    nonlocal header_index
                    args = match.group(1).strip()
                    if 'random.randint' in args and not 'str(random.randint' in args:
                        return re.sub(r'random\.randint\(([^,]+), ([^)]+)\)', r'str(random.randint(\1, \2))',
                                      match.group(0))
                    if 'str(' in args:
                        return match.group(0)
                    if header_index >= len(headers):
                        return match.group(0)
                    if ',' in args:
                        first_arg, second_arg = args.split(',', 1)
                        new_second_arg = f'str({headers[header_index]})'
                        header_index += 1
                        return f'.fill({first_arg.strip()}, {new_second_arg})'
                    else:
                        new_arg = f'str({headers[header_index]})'
                        header_index += 1
                        return f'.fill({new_arg})'

                def replace_click(match):
                    nonlocal header_index
                    args = match.group(1).strip()
                    if 'str(' in args:
                        return match.group(0)
                    if header_index >= len(headers):
                        return match.group(0)
                    new_arg = f'str({headers[header_index]})'
                    header_index += 1
                    return f'page.get_by_text({new_arg})'

                updated_code = fill_pattern.sub(replace_fill, code)
                updated_code = click_pattern.sub(replace_click, updated_code)

                with open(file_path, 'w') as file:
                    file.write(updated_code)
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

        def replace_goto_calls(file_path):
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                code = ''.join(lines)
                goto_pattern = re.compile(r'page\.goto\((.*?)\)', re.DOTALL)
                updated_code = goto_pattern.sub('page.goto(base_url)', code)
                with open(file_path, 'w') as file:
                    file.write(updated_code)
            except Exception as e:
                print(f"Error replacing goto calls in {file_path}: {e}")

        def find_csv_base_names(directory):
            csv_base_names = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.csv'):
                        base_name = os.path.splitext(file)[0]
                        csv_base_names.append(os.path.relpath(os.path.join(root, base_name), directory))
            return csv_base_names

        def process_script_with_ast(script_path, updated_script_path, csv_path, script_name):
            logging.info(f"Processing script: {script_path}")

            try:
                with open(script_path, 'r') as file:
                    script_content = file.read()

                comments = extract_comments(script_content)
                fill_data = extract_fill_data(script_path)
                save_data_to_csv([fill_data], csv_path)

                tree = ast.parse(script_content)
                static_code = []
                function_name = extract_function_name(script_content)

                comment_lines = sorted(comments.keys())
                current_comment_index = 0

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        function_name = node.name
                        if not function_name.startswith('test_'):
                            function_name = function_name.replace('test_', '')
                    elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                        func = node.value.func
                        if isinstance(func, ast.Attribute):
                            if not (func.attr == 'close' and func.value.id in {'browser', 'context'}):
                                line_number = node.lineno
                                static_code.append(astor.to_source(node).strip())
                                while current_comment_index < len(comment_lines) and comment_lines[
                                    current_comment_index] <= line_number:
                                    static_code.insert(len(static_code) - 1,
                                                       comments[comment_lines[current_comment_index]])
                                    current_comment_index += 1
                column_names, csv_data = read_values_from_csv(csv_path)
                param_names = ', '.join(column_names)
                static_code_str = '\n    '.join(static_code)

                db_operations_path = get_file_location('database_operations.py')
                method_name = f'{script_name}_data'
                if not method_name.startswith('test_'):
                    method_name = method_name.replace(method_name, 'test_' + method_name)
                if not method_exists(db_operations_path, method_name):
                    add_method(db_operations_path, method_name)
                updated_script_content = f"""import pytest
import random
import pandas as pd
import allure
from database.database_operations import *
from playwright.sync_api import Page, expect


def read_values_from_csv():
    df = pd.read_csv(r'{csv_path}')
    return df.values.tolist()


csv_data = read_values_from_csv()


@allure.feature('{script_name}')
@allure.story('{script_name}')
@allure.title('{script_name}')
@pytest.mark.parametrize('{param_names}', csv_data)
def test_{function_name}(page: Page, {', '.join(column_names)}, base_url) -> None:
    {static_code_str}
"""

                with open(updated_script_path, 'w') as file:
                    file.write(updated_script_content)

                logging.info(f"Updated script saved to {updated_script_path}")

            except Exception as e:
                logging.error(f"Error processing script {script_path}: {e}")

        def replace_scripts(directory):
            csv_base_names = find_csv_base_names(directory)

            for base_name in csv_base_names:
                csv_file_path = os.path.join(directory, f'{base_name}.csv')
                python_file_path = os.path.join(directory, f'{base_name}.py')

                if os.path.isfile(csv_file_path) and os.path.isfile(python_file_path):
                    headers = get_csv_headers(csv_file_path)
                    if headers:
                        replace_arguments(python_file_path, headers)
                        replace_goto_calls(python_file_path)

        def parse_scripts(golden_scripts, system_generated_scripts):

            script_count = 0
            csv_count = 0

            for root, dirs, files in os.walk(golden_scripts):
                for script_file in files:
                    if script_file.endswith('.py'):
                        script_path = os.path.join(root, script_file)
                        relative_path = os.path.relpath(script_path, golden_scripts)
                        updated_script_path = os.path.join(system_generated_scripts, relative_path)
                        updated_script_dir = os.path.dirname(updated_script_path)
                        os.makedirs(updated_script_dir, exist_ok=True)
                        csv_path = os.path.join(updated_script_dir, f'{os.path.splitext(script_file)[0]}.csv')

                        process_script_with_ast(script_path, updated_script_path, csv_path,
                                                os.path.splitext(script_file)[0])

                        script_count += 1
                        csv_count += 1

            logging.info(f"Scripts have been parsed, updated, and saved successfully.")
            logging.info(f"Total scripts generated: {script_count}")
            logging.info(f"Total CSV files generated: {csv_count}")

            print(f"Total scripts updated: {script_count}")
            print(f"Total CSV files generated: {csv_count}")

        log_file = setup_logging()
        parse_scripts(golden_script_dir, system_generated_scripts_dir)
        replace_scripts(system_generated_scripts_dir)

        with open(log_file, 'a') as log:
            log.write('\n')

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
