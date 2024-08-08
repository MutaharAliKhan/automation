import os
import pandas as pd
import re
import ast
import astor
import logging


script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
log_dir = os.path.join(project_root, 'logs')
log_file = os.path.join(log_dir, 'parser.log')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

recorded_scripts_dir = os.path.join(project_root, 'recorded_scripts')
updated_scripts_dir = os.path.join(project_root, 'updated_scripts')
os.makedirs(updated_scripts_dir, exist_ok=True)

script_count = 0
csv_count = 0


def sanitize_name(name: str) -> str:
    name = (name.replace("data-e2e", "").replace("data-test", "")
            .replace("input", "").replace("type", ""))
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    return name


def extract_string_literals(code_line):
    pattern = r"'(?:\\'|[^'])*'|\"(?:\\\"|[^\"])*\""
    matches = re.findall(pattern, code_line)
    strings = [re.sub(r"(^'|'$)|(^\"|\"$)", "", match).replace("\\'", "'").replace('\\"', '"') for match in matches]
    return strings


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

        for line in result:
            extracted_lines_strings = extract_string_literals(line[1])
            column_name = sanitize_name(str(extracted_lines_strings[0]))

            if column_name in column_count:
                column_count[column_name] += 1
                unique_column_name = f"{column_name}{column_count[column_name]}"
            else:
                column_count[column_name] = 0
                unique_column_name = column_name

            column_list.append(unique_column_name)
            value = sanitize_name(str(extracted_lines_strings[1]))
            fill_data[unique_column_name] = value
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
        pattern = rf'#\bdef {method_name}\('
        if re.search(pattern, content):
            return True
    except Exception as e:
        logging.error(f"Error checking method existence in file {file_path}: {e}")

    return False


def add_method(file_path, method_name):
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

        if method_code in content:
            logging.info(f"Method '{method_name}' already exists in {file_path}.")
            return

        imports_needed = """import pandas as pd
from database.Queries import *
from database.database_connection import *"""

        if imports_needed not in content:
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

    for index, line in enumerate(lines):
        stripped_line = line.strip()

        if in_multiline_comment:
            if stripped_line.endswith("'''") or stripped_line.endswith('"""'):
                multiline_comment_lines.append(stripped_line)
                comments[index + 1] = '\n       '.join(multiline_comment_lines)
                in_multiline_comment = False
                multiline_comment_lines = []
            else:
                multiline_comment_lines.append(stripped_line)
        elif stripped_line.startswith("'''") or stripped_line.startswith('"""'):
            if stripped_line.endswith("'''") or stripped_line.endswith('"""'):
                comments[index + 1] = stripped_line
            else:
                multiline_comment_lines.append(stripped_line)
                in_multiline_comment = True
        elif stripped_line.startswith('#'):
            comments[index + 1] = stripped_line

    return comments


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
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                func = node.value.func
                if isinstance(func, ast.Attribute):
                    if not (func.attr == 'close' and func.value.id in {'browser', 'context'}):
                        line_number = node.lineno
                        # Add static code
                        static_code.append(astor.to_source(node).strip())

                        # Insert comments if available for this line
                        while current_comment_index < len(comment_lines) and comment_lines[current_comment_index] <= line_number:
                            # Add comment before the static code
                            static_code.insert(len(static_code) - 1, comments[comment_lines[current_comment_index]])
                            current_comment_index += 1

        column_names, csv_data = read_values_from_csv(csv_path)
        param_names = ', '.join(column_names) + ', base_url'
        static_code_str = '\n    '.join(static_code)

        db_operations_path = os.path.join(project_root, 'database', 'database_operations.py')
        method_name = f'{script_name}_data'
        if not method_exists(db_operations_path, method_name):
            add_method(db_operations_path, method_name)

        updated_script_content = (
            "import pytest\n"
            "import pandas as pd\n"
            "import allure\n"
            "from database.database_operations import *\n"
            "from playwright.sync_api import Page, expect\n\n\n"
            "\n\ntest_data = read_json(r" + "'" + os.path.join(project_root, 'database', 'test_data.json') + "'" + ")"
            "\n\n\ndef read_values_from_csv():\n"
            f"    df = pd.read_csv(r'{csv_path}')\n"
            "    return df.values.tolist()\n\n\n"
            "csv_data = read_values_from_csv()\n\n\n"
            f"@allure.feature('{script_name}')\n"
            f"@allure.story('{script_name}')\n"
            f"@allure.title('{script_name}')\n"
            f"@pytest.mark.parametrize('{param_names}', csv_data)\n"
            f"def test_{function_name}(page: Page, {', '.join(column_names)}, base_url) -> None:\n"
            f"    {static_code_str}\n"
        )

        with open(updated_script_path, 'w') as file:
            file.write(updated_script_content)

        logging.info(f"Updated script saved to {updated_script_path}")

    except Exception as e:
        logging.error(f"Error processing script {script_path}: {e}")


for script_file in os.listdir(recorded_scripts_dir):
    script_path = os.path.join(recorded_scripts_dir, script_file)

    if os.path.isfile(script_path):
        script_name = os.path.splitext(script_file)[0]
        updated_script_path = os.path.join(updated_scripts_dir, script_file)
        csv_path = os.path.abspath(os.path.join(updated_scripts_dir, f'{script_name}.csv'))

        process_script_with_ast(script_path, updated_script_path, csv_path, script_name)

        script_count += 1
        csv_count += 1

logging.info(f"Scripts have been parsed, updated, and saved successfully.")
logging.info(f"Total scripts updated: {script_count}")
print(f"Total scripts updated: {script_count}")
logging.info(f"Total CSV files generated: {csv_count}")
print(f"Total CSV files generated: {csv_count}")

with open(log_file, 'a') as log:
    log.write('\n')