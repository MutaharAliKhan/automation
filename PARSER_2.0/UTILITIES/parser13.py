import ast
import csv
import re
import time
import logging
from utils.utils import *
import pandas as pd
from collections import defaultdict


def setup_logging():
    log_dir = get_root_path_join('logs')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'parser.log')

    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return log_file


def rename_scripts(directory):
    try:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.py') and not filename.startswith('test_'):
                    new_filename = f'test_{filename}'
                    old_path = os.path.join(root, filename)
                    new_path = os.path.join(root, new_filename)
                    os.rename(old_path, new_path)
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


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


def sanitize_locator(name):
    try:
        name = (name.replace("data-e2e", "")
                .replace("data-test", "")
                .replace("input", "")
                .replace("type", ""))
        name = re.sub(r'[^a-zA-Z0-9_]', '', name)
        return name
    except Exception as e:
        print(f"An error occurred during sanitization: {e}")
        return None


# This method is not using anywhere
def save_data_to_csv(data, csv_path):
    try:
        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False)
        logging.info(f"Data saved to CSV at {csv_path}")
    except Exception as e:
        logging.error(f"Error saving data to CSV at {csv_path}: {e}")


# This method is not using anywhere
def extract_function_name(script_content):
    match = re.search(r'def (\w+)\(', script_content)
    return match.group(1) if match else 'run'


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


def convert_list_to_dict(column_names, values):
    result = {}
    for i, column in enumerate(column_names):
        if i < len(values[0]):
            result[column] = f"{values[0][i]}"
        else:
            result[column] = None
    return result


def replace_multiple_variables(original_dict, replacement_dict, indent=12):
    indent_space = ' ' * indent
    formatted_result = "{\n" + ",\n".join(
        [
            f"{indent_space}'{k}': {replacement_dict[k]}" if k in replacement_dict else f"{indent_space}'{k}': '{v}'"
            for k, v in original_dict.items()]
    ) + "\n                 }"

    return formatted_result


def add_method(file_path, method_name, column_values):
    values = convert_list_to_dict(column_values[0], column_values[1])
    replacement_dict = {
        'get_text_value': f'current_branch_code',
    }
    formatted_dict = replace_multiple_variables(values, replacement_dict)

    method_code = f"""

\ndef {method_name}():\n
    result = execute_query(int(current_branch_code), Queries.fetch_customer,
                           values=(current_branch_code, "586", "81"))

    if isinstance(result, list):
        data = [{formatted_dict} for row in result]
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


def generate_database_operation_method(csv_path, script_name):
    column_header_value = read_values_from_csv(csv_path)
    method_name = f'{script_name}_data'
    func_name = method_name.removeprefix('test_')
    db_operations_path = get_root_path_join('database', 'database_operations.py')
    if not method_exists(db_operations_path, func_name):
        add_method(db_operations_path, func_name, column_header_value)


def read_values_from_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)
        values = df.values.tolist()
        return df.columns.tolist(), values
    except Exception as e:
        logging.error(f"Error reading values from CSV at {csv_path}: {e}")
        return [], []


def extract_page_lines_and_comments(script_content, exclude_keywords=None):
    tree = ast.parse(script_content)
    page_lines = []
    single_line_comments = []
    multi_line_comments = []
    excluded_lines = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) or isinstance(node, ast.Assign):
            code_line = ast.get_source_segment(script_content, node)
            if 'page.' in code_line:
                if exclude_keywords and any(keyword in code_line for keyword in exclude_keywords):
                    excluded_lines.append((node.lineno, code_line.strip()))
                else:
                    page_lines.append((node.lineno, code_line.strip()))

    for lineno, line in enumerate(script_content.splitlines(), 1):
        stripped_line = line.strip()
        if stripped_line.startswith('#'):
            single_line_comments.append((lineno, stripped_line))

    multi_line_comment_pattern = re.compile(r"'''(.*?)'''|\"\"\"(.*?)\"\"\"", re.DOTALL)
    for match in multi_line_comment_pattern.finditer(script_content):
        comment = match.group(1) if match.group(1) else match.group(2)
        start_lineno = script_content[:match.start()].count('\n') + 1
        end_lineno = start_lineno + comment.count('\n') + 1
        multi_line_comments.append((start_lineno, end_lineno, '"""' + comment.strip() + '"""'))

    return page_lines, single_line_comments, multi_line_comments, excluded_lines


def formate_lines(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    pattern = re.compile(
        r'(\.(?:locator|get_by_text)\([^)]*\)\s*\.\s*fill\([^)]*?\))',
        re.DOTALL
    )

    def join_multiline(match):
        joined_line = ''.join(match.group(1).splitlines())
        return re.sub(r'\s+', '', joined_line)

    joined_code = pattern.sub(join_multiline, code)
    with open(file_path, 'w') as file:
        file.write(joined_code)


def extract_and_replace_fill_values(script_content):
    class AST_Visitor(ast.NodeVisitor):
        def __init__(self):
            self.lines = []
            self.values = []
            self.locators = []
            self.updated_lines = []
            self.locator_count = defaultdict(int)
            self.ignore_lines = set()

        def get_string_value(self, node):
            if isinstance(node, ast.Str):
                return node.s
            elif isinstance(node, ast.Call):
                if any(keyword in ast.unparse(node.func) for keyword in ['str', 'random', 'randint']):
                    return None
                else:
                    return self.get_string_value(node.args[0])
            elif isinstance(node, ast.Num):
                return node.n
            return None

        def get_function_name(self, node):
            if isinstance(node, ast.Name):
                return node.id
            elif isinstance(node, ast.Attribute):
                return self.get_function_name(node.value)
            return None

        def _generate_unique_locator(self, variable_name):
            occurrence_index = self.locator_count[variable_name]
            unique_locator = f'{variable_name}{occurrence_index}' if occurrence_index > 0 else variable_name
            self.locator_count[variable_name] += 1
            return unique_locator

        @staticmethod
        def replace_string_literal(original_line, var_name, value):
            updated_line = original_line.replace(f"'{value}'", f'str({var_name})')
            updated_line = updated_line.replace(f'"{value}"', f'str({var_name})')
            return updated_line

        def add_value_and_locator(self, value, locator):
            self.values.append(value)
            self.locators.append(locator)

        def track_updated_line(self, node, updated_line):
            self.lines.append((node.lineno, updated_line))
            self.updated_lines.append((node.lineno, updated_line))

        def visit_Call(self, node):
            line_number = node.lineno
            if any(line.strip().startswith('expect') for line in
                   script_content.splitlines()[line_number - 1:line_number]):
                return

            if isinstance(node.func, ast.Attribute):
                method_name = node.func.attr
                locator_node = node.func.value

                if method_name == 'fill' and isinstance(locator_node, ast.Call):
                    if hasattr(locator_node.func, 'attr') and locator_node.func.attr == 'get_by_text':
                        value_node = locator_node.args[0] if locator_node.args else None
                        fill_value_node = node.args[0] if node.args else None

                        get_text_value = self.get_string_value(value_node)
                        fill_value = self.get_string_value(fill_value_node)

                        get_by_text_var = self._generate_unique_locator('get_text_value')
                        get_fill_value_var = self._generate_unique_locator('get_fill_value')

                        if get_text_value is not None:
                            self.add_value_and_locator(get_text_value, get_by_text_var)

                        if fill_value is not None:
                            self.add_value_and_locator(fill_value, get_fill_value_var)

                        updated_line = script_content.splitlines()[node.lineno - 1].strip()
                        if get_text_value:
                            updated_line = self.replace_string_literal(updated_line, get_by_text_var, get_text_value)

                        if fill_value:
                            updated_line = self.replace_string_literal(updated_line, get_fill_value_var, fill_value)

                        self.track_updated_line(node, updated_line)
                        return

                if method_name == 'fill':
                    value_node = node.args[1] if method_name == 'fill' and len(node.args) == 2 else node.args[0] \
                        if node.args else None

                    fill_value = self.get_string_value(value_node)

                    if value_node is not None:
                        if node.args:
                            locator_str = ast.get_source_segment(script_content, node.func.value.args[0]) if isinstance(
                                locator_node, ast.Call) else ast.get_source_segment(script_content, node.args[0])
                        else:
                            locator_str = None

                        sanitized_locator = sanitize_locator(str(locator_str))
                        self.locator_count[sanitized_locator] += 1

                        if self.locator_count[sanitized_locator] > 1:
                            sanitized_locator = f"{sanitized_locator}{self.locator_count[sanitized_locator] - 1}"

                        if fill_value is not None:
                            self.add_value_and_locator(fill_value, sanitized_locator)

                        updated_line = ast.get_source_segment(script_content, node)
                        updated_line = self.replace_string_literal(updated_line, sanitized_locator, fill_value)
                        self.track_updated_line(node, updated_line)

                elif method_name == 'get_by_text':
                    value_node = node.args[0] if node.args else None
                    get_text_value = self.get_string_value(value_node)

                    get_fill_value_var = self._generate_unique_locator('get_text_value')

                    if get_text_value is not None:
                        self.add_value_and_locator(get_text_value, get_fill_value_var)

                        full_line = script_content.splitlines()[node.lineno - 1].strip()
                        updated_line = self.replace_string_literal(full_line, get_fill_value_var, get_text_value)
                        self.track_updated_line(node, updated_line)


                elif method_name == 'filter':
                    has_text_arg = next((kwarg for kwarg in node.keywords if kwarg.arg == 'has_text'), None)
                    if has_text_arg and isinstance(has_text_arg.value, ast.Str):
                        has_text = self.get_string_value(has_text_arg.value)
                        if has_text_arg.value is not None:
                            if isinstance(locator_node, ast.Call):
                                locator_str = ast.get_source_segment(script_content, node.func.value.args[0])
                            else:
                                if node.args:
                                    locator_str = ast.get_source_segment(script_content, node.args[0])
                                else:
                                    locator_str = None

                            if locator_str is not None:
                                sanitized_locator = sanitize_locator(str(locator_str))
                                self.locator_count[sanitized_locator] += 1

                                if self.locator_count[sanitized_locator] > 1:
                                    sanitized_locator = f"{sanitized_locator}{self.locator_count[sanitized_locator] - 1}"

                                self.add_value_and_locator(has_text, sanitized_locator)
                                full_line = script_content.splitlines()[node.lineno - 1].strip()
                                updated_line = self.replace_string_literal(full_line, sanitized_locator, has_text)
                                self.track_updated_line(node, updated_line)

                elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value,
                                                                         ast.Name) and node.func.value.id == 'random' and node.func.attr == 'randint':
                    if len(node.args) == 2 and all(isinstance(arg, ast.Constant) for arg in node.args):
                        start = node.args[0].value
                        end = node.args[1].value
                        updated_line = script_content.splitlines()[node.lineno - 1].strip()
                        original_call = f'random.randint({start}, {end})'
                        str_call = f'str(random.randint({start}, {end}))'
                        if original_call in updated_line and str_call not in updated_line:
                            updated_line = updated_line.replace(original_call, str_call)
                            self.track_updated_line(node, updated_line)

                        return

            self.generic_visit(node)

    tree = ast.parse(script_content)
    visitor = AST_Visitor()
    visitor.visit(tree)

    return visitor.lines, visitor.values, visitor.locators, visitor.updated_lines


def create_csv_file(locators, values, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=locators)
        writer.writeheader()
        writer.writerow(dict(zip(locators, values)))


def generate_updated_script(original_lines, updated_lines):
    updated_lines_dict = dict(updated_lines)
    original_lines_dict = dict(original_lines)
    all_lines = {**original_lines_dict, **updated_lines_dict}
    sorted_lines = [all_lines[lineno] for lineno in sorted(all_lines)]

    return '\n    '.join(sorted_lines)


def process_script_with_ast(script_content_path, updated_script_path, csv_path, script_name):
    try:

        """Read the script content from the file"""
        with open(script_content_path, 'r') as f:
            script_content = f.read()

        """Extract relevant information from the script"""
        page_lines, single_line_comments, multi_line_comments, excluded_lines = extract_page_lines_and_comments(
            script_content)
        lines_with_methods, values, locators, updated_lines = extract_and_replace_fill_values(script_content)

        """Create CSV file from the extracted data & Read values from the created CSV file"""
        create_csv_file(locators, values, csv_path)
        csv_headers, csv_values = read_values_from_csv(csv_path)

        """Generate updated script lines"""
        updated_script = generate_updated_script(page_lines + single_line_comments, updated_lines)

        """Combine all multi-line comments into a single string"""
        multiline_comment_lines = ""
        for start_lineno, end_lineno, comment in multi_line_comments:
            multiline_comment_lines += f"{comment}\n"

        """Prepare the parameterized parameters string for pytest"""
        parametrize_params = ', '.join(locators)

        """ Generate the updated script content"""
        updated_script_content = f"""{multiline_comment_lines}
import pytest
import random
import pandas as pd
import allure

from database.database_operations import *
from playwright.sync_api import Page, expect
from utils.pre_req_test import pre_req_user_setup

def read_values_from_csv():
    pre_req_user_setup()
    df = pd.read_csv(f"{{os.path.dirname((__file__))}}"+r'\\{script_name}.csv')
    return df.values.tolist()

csv_data = read_values_from_csv()

@allure.feature('{script_name.replace('test_', '')}')
@allure.story('{script_name.replace('test_', '')}')
@allure.title('{script_name.replace('test_', '')}')
@pytest.mark.parametrize('{parametrize_params}', csv_data)
def {script_name}(page: Page, {', '.join(csv_headers)}, base_url) -> None:
    update_system_ip()
    {updated_script}
"""

        """ Write the updated script content to the specified path"""
        with open(updated_script_path, 'w') as file:
            file.write(updated_script_content)

        logging.info(f"Updated script saved to {updated_script_path}")

    except Exception as e:
        logging.error(f"Error processing script {script_content_path}: {e}")


def runner(input_dir, output_dir):
    log_file = setup_logging()
    script_count = 0
    csv_count = 0
    os.makedirs(output_dir, exist_ok=True)

    start_time = time.time()

    rename_scripts(input_dir)
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, input_dir)
                script_name = os.path.splitext(file)[0]
                updated_script_path = os.path.join(output_dir, relative_path)
                csv_filename = f"{script_name}.csv"
                csv_path = os.path.join(output_dir, os.path.dirname(relative_path), csv_filename)

                os.makedirs(os.path.dirname(updated_script_path), exist_ok=True)
                os.makedirs(os.path.dirname(csv_path), exist_ok=True)

                """Final Processing"""
                process_script_with_ast(file_path, updated_script_path, csv_path, script_name)
                formate_lines(updated_script_path)
                replace_goto_calls(updated_script_path)
                generate_database_operation_method(csv_path, script_name)
                script_count += 1
                csv_count += 1

    end_time = time.time()
    total_time = end_time - start_time

    logging.info(f"Scripts have been parsed, updated, and saved successfully.")
    logging.info(f"Total scripts updated: {script_count}")
    logging.info(f"Total CSV files generated: {csv_count}")
    logging.info(f"Total time taken: {total_time:.2f} seconds")
    print(f"Total time taken: {total_time:.2f} seconds")

    with open(log_file, 'a') as log:
        log.write('\n')


input_directory = r'D:\MyRecentProjects\Data_Utility\golden_scripts'
output_directory = r'D:\MyRecentProjects\Data_Utility\golden_scripts2'

runner(input_directory, output_directory)
