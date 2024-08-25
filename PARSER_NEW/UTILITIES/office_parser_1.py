import os
import random
import time
from tkinter import messagebox

import pandas as pd
import re
import ast
import astor
import logging
import tkinter as tk
from utils.utils import get_folder_location

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir))
log_dir = os.path.join(project_root, 'logs')
log_file = os.path.join(log_dir, 'parser.log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def replace_goto_calls(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    code = ''.join(lines)
    goto_pattern = re.compile(r'page\.goto\(([^)]+)\)', re.DOTALL)
    updated_code = goto_pattern.sub(r'page.goto(base_url)', code)
    with open(file_path, 'w') as file:
        file.write(updated_code)


def sanitize_name(name: str) -> str:
    name = (name.replace("data-e2e", "").replace("data-test", "")
            .replace("input", "").replace("type", ""))
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    return name


def extract_cleaned_string_literals(code_line):
    pattern = r"'(?:\\'|[^'])*'|\"(?:\\\"|[^\"])*\""
    matches = re.findall(pattern, code_line)
    strings = [re.sub(r"(^'|'$)|(^\"|\"$)", "", match).replace("\\'", "'").replace('\\"', '"') for match in matches]
    return strings


def extract_complete_string_literals(code_line):
    pattern = r"'(?:\\'|[^'])*'|\"(?:\\\"|[^\"])*\""
    matches = re.findall(pattern, code_line)
    return matches


def find_replaceable_lines(filepath):
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        for line_number, line in enumerate(lines, start=1):
            if ('fill' in line or 'get_by_text' in line or 'filter' in line) and (
                    all(keyword not in line for keyword in
                        ('str(', 'random', 'randint', 'expect('))):
                results.append((line_number, line.strip()))
    except Exception as e:
        logging.error(f"Error reading file {filepath}: {e}")
    return results


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
            result[column] = f"'{values[0][i]}'"
        else:
            result[column] = None
    return result


def pre_defined_variables(list_values):
    list_values['brncd'] = 'current_branch_code'
    list_values['usernamebox'] = 'username'
    list_values['passwordbox'] = 'password'
    list_values['PasswordTextBox'] = 'password'
    list_values['AmountTextBox'] = 'random.randint(1000, 9999)'
    list_values['NarrationTextBox'] = "'Automation NarrationTextBox'"
    list_values['NoLabelNarration2TextBox'] = "'Automation NarrationTextBox2'"
    list_values['NoLabelNarration3TextBox'] = "'Automation NarrationTextBox3'"
    list_values['CustomerNameTextBox'] = "'Playwright Automation'"
    list_values['ChequeDateTextBox'] = "row['TDATE']"
    list_values['RemarksTextAreaRemarksTextArea'] = "'Automation Remarks'"

    return list_values


def add_method(file_path, method_name, column_values):
    column_formate = convert_list_to_dict(column_values[0], column_values[1])
    key_value_pairs = pre_defined_variables(column_formate)
    updated_values_format = "{\n" + ",\n".join(
        [f"              '{k}': {v}" for k, v in key_value_pairs.items()]) + "\n             }"
    method_code = f"""

\ndef {method_name}():\n# System Generated Method kindly modified it before use
    result = execute_query(int(current_branch_code), Queries.fetch_customer,
                           values=(current_branch_code, "586", "81"))

    if isinstance(result, list):
        data = [{updated_values_format} for row in result]
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
    for index, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith('#'):
            comments[index + 1] = '\n' + '    ' + stripped_line

    return comments


def read_values_from_csv(csv_path):
    try:
        df = pd.read_csv(csv_path)
        values = df.values.tolist()
        return df.columns.tolist(), values
    except Exception as e:
        logging.error(f"Error reading values from CSV at {csv_path}: {e}")
        return [], []


def process_script_with_ast(script_path, updated_script_path, csv_path, script_name):
    logging.info(f"Processing script: {script_path}")

    try:
        with open(script_path, 'r') as file:
            script_content = file.read()
        multiline_comment_lines = ""
        comments = extract_comments(script_content)

        tree = ast.parse(script_content.strip())
        static_code = []
        function_name = extract_function_name(script_content)

        comment_lines = sorted(comments.keys())
        current_comment_index = 0

        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                multiline_comment_lines += f"{node.value.s}\n"
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                if not function_name.startswith('test_'):
                    function_name = 'test_' + function_name
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                func = node.value.func
                if isinstance(func, ast.Attribute):
                    if not (func.attr == 'close' and func.value.id in {'browser', 'context'}):
                        line_number = node.lineno
                        static_code.append(astor.to_source(node).strip())
                        while current_comment_index < len(comment_lines) and comment_lines[
                            current_comment_index] <= line_number:
                            static_code.insert(len(static_code) - 1, comments[comment_lines[current_comment_index]])
                            current_comment_index += 1

        column_names, csv_data = read_values_from_csv(csv_path)
        param_names = ', '.join(column_names)
        static_code_str = '\n    '.join(static_code)
        top_comment = f'"""{multiline_comment_lines}"""'

        updated_script_content = f"""
{top_comment}        
import pytest
import random
import pandas as pd
import allure

from database.database_operations import *
from playwright.sync_api import Page, expect\n
from utils.pre_req_test import pre_req_user_setup

def read_values_from_csv():
    pre_req_user_setup()
    df = pd.read_csv(f"{{os.path.dirname((__file__))}}"+r'\\{script_name}.csv')
    return df.values.tolist()\n

csv_data = read_values_from_csv()\n

@allure.feature('{script_name.replace('test_', '')}')
@allure.story('{script_name.replace('test_', '')}')
@allure.title('{script_name.replace('test_', '')}')
@pytest.mark.parametrize('{param_names}', csv_data)
def {script_name}(page: Page, {', '.join(column_names)}, base_url) -> None:
    update_system_ip()
    {static_code_str}\n
"""

        with open(updated_script_path, 'w') as file:
            file.write(updated_script_content)

        logging.info(f"Updated script saved to {updated_script_path}")

    except Exception as e:
        logging.error(f"Error processing script {script_path}: {e}")


def get_py_files(folder):
    py_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.py'):
                py_files.append([os.path.abspath(os.path.join(root, file)), file])
    return py_files



def rename_scripts(directory):
    try:
        py_files = get_py_files(directory)
        for filename in py_files:
            if not filename[1].startswith('test_'):
                new_filename = 'test_' + filename[1]
                old_path = filename[0]
                new_path = filename[0].replace(filename[1], new_filename)
                os.rename(old_path, new_path)
        return True
    except Exception as e:
        print(f"An error occurred while renaming files: {e}")
        logging.error(f"An error occurred while renaming files: {e}")
        return False


def unique_variable_name(name_list, value):
    count = 0
    unique_value = value
    while unique_value in name_list:
        count += 1
        unique_value = f"{value}_{count}"
    return unique_value


def get_lines_to_replace(file):
    all_matches = []
    csv_variables = []
    fill_data = {}
    try:
        result = find_replaceable_lines(file)
        for line in result:
            extracted_lines_strings = extract_complete_string_literals(line[1])
            extracted_lines_strings_with_out_quotes = extract_cleaned_string_literals(line[1])
            if len(extracted_lines_strings) == 1:
                get_by_txt = unique_variable_name(csv_variables, "get_by_txt")
                csv_variables.append(get_by_txt)
                fill_data[get_by_txt] = extracted_lines_strings_with_out_quotes[0]
                generated_line = (line[1].replace(extracted_lines_strings[0], f"str({get_by_txt})"))
                all_matches.append([line[1], generated_line])
            elif len(extracted_lines_strings) >= 2:
                if 'get_by_text' in line[1] and 'fill' in line[1]:
                    get_by_txt_data = unique_variable_name(csv_variables, "get_by_txt_data")
                    csv_variables.append(get_by_txt_data)
                    fill_data[get_by_txt_data] = extracted_lines_strings_with_out_quotes[0]
                    get_by_txt_data_val = unique_variable_name(csv_variables, "get_by_txt_data_val")
                    csv_variables.append(get_by_txt_data_val)
                    fill_data[get_by_txt_data_val] = extracted_lines_strings_with_out_quotes[1]
                    var_val = (line[1].replace(extracted_lines_strings[0], f'str({get_by_txt_data})')
                               .replace(extracted_lines_strings[1], f'str({get_by_txt_data_val})'))
                    all_matches.append([line[1], var_val])
                else:
                    column_name = sanitize_name(str(extracted_lines_strings_with_out_quotes[0]))
                    unique_column_name = unique_variable_name(csv_variables, column_name)

                    csv_variables.append(unique_column_name)
                    fill_data[unique_column_name] = extracted_lines_strings_with_out_quotes[1]
                    var_val = line[1].replace(extracted_lines_strings[1], f"str({unique_column_name})")
                    all_matches.append([line[1], var_val])
            else:
                print("More then 2 literals are found", line[1])
                logging.error("More then 2 literals are found", line[1])
        return all_matches, fill_data
    except Exception as e:
        print(f"Error extracting fill data from {file}: {e}")
        logging.error(f"Error extracting fill data from {file}: {e}")
        return []


def replace_strings_in_fileline(file_path, search_replace_list):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        with open(file_path, 'w') as file:
            for line in lines:
                for search, replace in search_replace_list:
                    if line.strip() == search:
                        file.writelines(f"    {replace}\n")
                        search_replace_list.remove([search, replace])
                        break
                else:
                    file.write(line)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        logging.error(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")


def replace_strings_in_fileline2(file_path, search_replace_list):
    try:
        with open(file_path, 'r') as file:
            lines = file.read()
        tree = ast.parse(lines)
        for search, replace in search_replace_list:
            for node in ast.walk(tree):
                if isinstance(node, ast.Expr) and isinstance(node.value, ast.Assign) and isinstance(node.value.value,
                                                                                                    ast.Str) and node.value.value.s.strip() == search:
                    node.value.value = ast.Str(replace, kind="")
                    break
            else:
                continue
            break
        with open(file_path, 'w') as file:
            file.write(astor.to_source(tree))
        print(f"File {file_path} modified successfully.")
        logging.info(f"File {file_path} modified successfully.")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        logging.error(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")


def formate_fill_lines_in_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()

    # Pattern to match split lines in `.locator().fill()` and `.get_by_text().fill()`
    pattern = re.compile(
        r'(\.(?:locator|get_by_text)\([^)]*\)\s*\.\s*fill\([^)]*?\))',
        re.DOTALL
    )

    def join_multiline(match):
        # Join all parts into a single line and remove excessive spacing
        joined_line = ''.join(match.group(1).splitlines())
        # Replace multiple spaces with a single space
        return re.sub(r'\s+', '', joined_line)

    # Substitute the multiline expressions with the joined version
    joined_code = pattern.sub(join_multiline, code)

    with open(file_path, 'w') as file:
        file.write(joined_code)


def generate_databaseOperation_method(csv_path, script_name):
    column_header_value = read_values_from_csv(csv_path)
    method_name = f'{script_name}_data'
    func_name = method_name.removeprefix('test_')
    db_operations_path = os.path.join(project_root, 'database', 'database_operations.py')
    if not method_exists(db_operations_path, func_name):
        add_method(db_operations_path, func_name, column_header_value)


def remove_expect_lines_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    with open(file_path, 'w') as file:
        for line in lines:
            if 'expect(' not in line.strip():
                file.write(line)


def Runner(source_dir, generation_dir):
    recorded_scripts_dir = source_dir
    updated_scripts_dir = generation_dir

    print("Source", recorded_scripts_dir)
    print("Destination", updated_scripts_dir)
    script_count = 0
    csv_count = 0

    rename_scripts(recorded_scripts_dir)
    for script_file in get_py_files(recorded_scripts_dir):
        script_path = script_file[0]
        if os.path.isfile(script_path):
            script_name = os.path.splitext(script_file[1])[0]
            updated_script_path = script_path.replace(recorded_scripts_dir, updated_scripts_dir)
            script_directory = updated_script_path.replace(script_file[1], "")
            if not os.path.exists(script_directory):
                os.makedirs(script_directory)
            path_csv = os.path.join(script_directory, f'{script_name}.csv')
            match_lines, fill_data, = get_lines_to_replace(script_path)
            save_data_to_csv([fill_data], path_csv)
            path_csv = path_csv.replace(os.path.dirname(updated_scripts_dir), '').removeprefix('\\')

            process_script_with_ast(script_path, updated_script_path, path_csv, script_name)
            formate_fill_lines_in_file(updated_script_path)
            replace_goto_calls(updated_script_path)
            match_lines2, fill_data, = get_lines_to_replace(updated_script_path)
            replace_strings_in_fileline(updated_script_path, match_lines2)
            generate_databaseOperation_method(path_csv, script_name)
            script_count += 1
            csv_count += 1

    logging.info(f"Scripts have been parsed, updated, and saved successfully.")
    logging.info(f"Total scripts updated: {script_count}")
    print(f"Total scripts updated: {script_count}")
    logging.info(f"Total CSV files generated: {csv_count}")
    print(f"Total CSV files generated: {csv_count}")

    with open(log_file, 'a') as log:
        log.write('\n')


def execute(source_folder_name, destination_folder):
    if os.path.isfile(source_folder_name):
        messagebox.showerror('Python Error', 'Error: Source folder location should be a directory, not a file.')
        return
    if not os.path.isabs(source_folder_name):
        source_folder = get_folder_location(source_folder_name)
    else:
        source_folder = source_folder_name
    if not source_folder or not os.path.exists(source_folder):
        messagebox.showwarning('Python Warning', 'Warning: Source folder not found.')
        return
    if not os.path.isabs(destination_folder):
        destination_folder_path = os.path.join(os.path.dirname(source_folder), destination_folder)
    else:
        destination_folder_path = destination_folder
    if not os.path.exists(os.path.dirname(destination_folder_path)):
        os.makedirs(destination_folder_path, exist_ok=True)
    Runner(source_folder, destination_folder_path)


def Parser_UI():
    # Create main window
    window = tk.Tk()
    window.title("Playwright Parser Utility")
    window.configure(bg='#000000')
    # Create form
    frame = tk.Frame(window)
    frame.pack(padx=5, pady=5)

    # Add source folder label and entry
    source_label = tk.Label(frame, text="Source Folder Path/Name:", bg='#ffffff', fg='#003366',
                            font=("Helvetica", 12, 'bold'))
    source_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
    source_folder_field = tk.Entry(frame, width=50, bg='#f5f5f5', fg='#003366', font=("Helvetica", 12, 'bold'))
    source_folder_field.insert(0, "golden_scripts")
    source_folder_field.grid(row=0, column=1, padx=30, pady=10)

    # Add destination folder label and entry
    destination_label = tk.Label(frame, text="Destination Folder Name:", bg='#ffffff', fg='#003366',
                                 font=("Helvetica", 12, 'bold'))
    destination_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
    destination_folder_field = tk.Entry(frame, width=50, bg='#f5f5f5', fg='#003366', font=("Helvetica", 12, 'bold'))
    destination_folder_field.insert(0, "system_generated_scripts")
    destination_folder_field.grid(row=1, column=1, padx=30, pady=10)

    def generate():
        start_time = time.time()
        source_folder_name = source_folder_field.get().strip('"').strip("'")
        destination_folder = destination_folder_field.get().strip('"').strip("'")
        if not source_folder_name or not destination_folder:
            messagebox.showerror('Error', 'Error: Source and destination folders are required.', bg='#003366',
                                 fg='#ffffff')
            return
        execute(source_folder_name, destination_folder)
        end_time = time.time()
        elapsed_time = end_time - start_time
        source_folder_field.delete(0, tk.END)
        destination_folder_field.delete(0, tk.END)
        window.destroy()
        messagebox.showinfo("Result", f"The parser is executed in {elapsed_time:.2f} seconds.")

    generate_button = tk.Button(frame, text="Generate", command=generate, bg='#007bff', fg='white',
                                font=("Helvetica", 14, 'bold'), relief=tk.FLAT)
    generate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

    # Run window
    window.mainloop()


Parser_UI()
