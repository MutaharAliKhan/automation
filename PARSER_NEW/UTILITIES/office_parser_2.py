import os
import time
from screeninfo.screeninfo import get_monitors
from tqdm import tk
import tkinter as tk
from tkinter import messagebox
import csv
import os
import re
import logging
import ast
import astor
import pandas as pd

BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[91m'
ORANGE = '\033[38;5;208m'
RESET = '\033[0m'
CYAN = '\033[96m'


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


def parser(golden_script_dir, system_generated_scripts_dir):
    try:

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
                    # if line.lstrip().startswith('expect(page.get_by_text('):
                    #     continue
                    # if line.lstrip().startswith('expect('):
                    #     continue

                    if 'get_by_text' in line:
                        get_by_text_part = re.search(r"get_by_text\((.*?)\)", line)
                        if get_by_text_part:
                            extracted_text = extract_string_literals(get_by_text_part.group(1))
                            if len(extracted_text) < 1:
                                continue

                            column_name = 'get_fill_text'
                            value = str(extracted_text[0])

                            if column_name in column_count:
                                column_count[column_name] += 1
                                unique_column_name = f"{column_name}{column_count[column_name]}"
                            else:
                                column_count[column_name] = 1
                                unique_column_name = column_name

                            column_list.append(unique_column_name)
                            text_data[unique_column_name] = value

                    if 'filter' in line and 'has_text=' in line:
                        filter_part = re.search(r"filter\(has_text\s*=\s*(.*?)\)", line)
                        if filter_part:
                            extracted_text = extract_string_literals(filter_part.group(1))
                            if len(extracted_text) < 1:
                                continue

                            column_name = 'filter_has_text'
                            value = str(extracted_text[0])

                            if column_name in column_count:
                                column_count[column_name] += 1
                                unique_column_name = f"{column_name}{column_count[column_name]}"
                            else:
                                column_count[column_name] = 1
                                unique_column_name = column_name

                            column_list.append(unique_column_name)
                            text_data[unique_column_name] = value

            except Exception as e:
                logging.error(f"Error extracting data from {file}: {e}")

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
                        value = str(extracted_lines_strings[1])

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

        def replace_multiple_variables(original_dict, replacement_dict, indent=12):
            indent_space = ' ' * indent
            formatted_result = "{\n" + ",\n".join(
                [
                    f"{indent_space}'{k}': {replacement_dict[k]}" if k in replacement_dict else f"{indent_space}'{k}': '{v}'"
                    for k, v in original_dict.items()]
            ) + "\n                 }"

            return formatted_result

        def add_method(file_path, method_name, values):
            replacement_dict = {
                'brncd': f"current_branch_code",
                'usernamebox': f"username",
                'passwordbox': f"password",
                'PasswordTextBox': f"password"
            }
            formatted_dict = replace_multiple_variables(values, replacement_dict)
            method_code = f"""
def {method_name}():
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

        def extract_comments(script_content):
            comments = {}
            lines = script_content.split('\n')

            for index, line in enumerate(lines):
                stripped_line = line.strip()

                if stripped_line.startswith('#'):
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
                #click_pattern = re.compile(r"get_by_text\(([^)]+)\)", re.DOTALL)
                click_pattern = re.compile(r'(?<!expect\()page\.get_by_text\(([^)]+)\)', re.DOTALL)
                filter_pattern = re.compile(r'filter\(has_text="?([^",)]+)"?\)', re.DOTALL)
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
                    if match.group(0).startswith('expect(page.get_by_text('):
                        return match.group(0)
                    nonlocal header_index
                    args = match.group(1).strip()
                    if 'str(' in args:
                        return match.group(0)
                    if header_index >= len(headers):
                        return match.group(0)
                    new_arg = f'str({headers[header_index]})'
                    header_index += 1
                    return f'page.get_by_text({new_arg})'

                def replace_filter(match):
                    nonlocal header_index
                    has_text_value = match.group(1).strip()
                    if 'str(' in has_text_value:
                        return match.group(0)
                    if header_index >= len(headers):
                        return match.group(0)
                    new_has_text_value = f'str({headers[header_index]})'
                    header_index += 1
                    return f'filter(has_text={new_has_text_value})'

                updated_code = fill_pattern.sub(replace_fill, code)
                updated_code = click_pattern.sub(replace_click, updated_code)
                updated_code = filter_pattern.sub(replace_filter, updated_code)

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

        def process_script_with_ast(script_path, updated_script_path, csv_path, updated_script_dir, script_name):
            updated_csv_path = csv_path.replace(updated_script_dir, '').removeprefix('\\')
            logging.info(f"Processing script: {script_path}")

            try:
                with open(script_path, 'r') as file:
                    script_content = file.read()

                multiline_comment_lines = ""
                comments = extract_comments(script_content)
                fill_data = extract_fill_data(script_path)
                save_data_to_csv([fill_data], csv_path)

                tree = ast.parse(script_content)
                static_code = []
                function_name = extract_function_name(script_content)

                comment_lines = sorted(comments.keys())
                current_comment_index = 0

                preserved_lines = []

                for node in ast.walk(tree):
                    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                        multiline_comment_lines += f"{node.value.s}\n"
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
                        elif isinstance(func, ast.Name) and func.id == 'expect':
                            if isinstance(node.value.args[0], ast.Call) and isinstance(
                                    node.value.args[0].func, ast.Attribute):
                                if node.value.args[0].func.attr == 'get_by_text':
                                    preserved_lines.append((node.lineno, astor.to_source(node).strip()))
                                else:
                                    static_code.append(astor.to_source(node).strip())

                column_names, csv_data = read_values_from_csv(csv_path)
                param_names = ', '.join(column_names)
                static_code_str = '\n    '.join(static_code)
                top_comment = f'"""{multiline_comment_lines}"""'

                preserved_lines_str = '\n'.join(line for _, line in preserved_lines)

                updated_script_content = f"""{top_comment}
import pytest
import random
import pandas as pd
from datetime import datetime
from database.database_operations import *
from playwright.sync_api import Page, expect
from utils.pre_req_test import pre_req_user_setup
current_data = datetime.now().strftime("%d/%m/%Y")


def read_values_from_csv():
    df = pd.read_csv(f"{{os.path.dirname((__file__))}}"+r'\\{script_name}.csv')
    return df.values.tolist()


csv_data = read_values_from_csv()



@pytest.mark.parametrize('{param_names}', csv_data)
def {script_name}(page: Page, {', '.join(column_names)}, base_url) -> None:
    pre_req_user_setup()
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
                updated_script_path = os.path.join(directory, f'{base_name}.py')

                if os.path.isfile(csv_file_path) and os.path.isfile(updated_script_path):
                    headers = get_csv_headers(csv_file_path)
                    if headers:
                        replace_arguments(updated_script_path, headers)
                        replace_goto_calls(updated_script_path)

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
                        complete_csv_path = os.path.abspath(os.path.join(system_generated_scripts, csv_path))

                        process_script_with_ast(script_path, updated_script_path, csv_path,
                                                updated_script_dir, os.path.splitext(script_file)[0])

                        script_count += 1
                        csv_count += 1

            logging.info(f"Scripts have been parsed, updated, and saved successfully.")
            logging.info(f"Total scripts generated: {script_count}")
            logging.info(f"Total CSV files generated: {csv_count}")

            print(f"Total scripts updated: {script_count}")
            print(f"Total CSV files generated: {csv_count}")

        parse_scripts(golden_script_dir, system_generated_scripts_dir)
        replace_scripts(system_generated_scripts_dir)



        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False



def get_base_paths(system_generated_scripts_dir):
    golden_scripts_dir = r'D:\MyRecentProjects\Data_Utility\golden_scripts'
    if not os.path.exists(system_generated_scripts_dir):
        os.makedirs(system_generated_scripts_dir, exist_ok=True)
    return golden_scripts_dir, system_generated_scripts_dir


def run_all_utilities(system_generated_scripts_dir):
    golden_scripts_dir, system_generated_scripts_dir = get_base_paths(system_generated_scripts_dir)
    utilities = [
        (lambda: rename_scripts(golden_scripts_dir), "rename_scripts"),
        (lambda: parser(golden_scripts_dir, system_generated_scripts_dir), "parser"),
    ]

    all_success = True
    start_time = time.time()

    for utility_func, description in utilities:
        print(f"{ORANGE}Running {description}...{RESET}")
        try:
            success = utility_func()
            print(f"{ORANGE}{description} returned: {BOLD}{GREEN}{success}{RESET}")
            if not success:
                print(f"{BOLD}{RED}{description} failed.{RED}{RESET}")
                all_success = False
        except Exception as e:
            print(f"{BOLD}{RED}Exception occurred during {description}: {e}{RESET}")
            all_success = False

    end_time = time.time()
    elapsed_time = end_time - start_time

    if all_success:
        print(f"\n{BOLD}{GREEN}The parser is executed in {CYAN}{elapsed_time:.2f}{RESET} {BOLD}{GREEN}seconds.{RESET}")
        messagebox.showinfo("Result", f"The parser is executed in {elapsed_time:.2f} seconds.")
    else:
        messagebox.showerror("Result", "Some utilities failed.")


def main():
    root = tk.Tk()
    root.title("Parser Utility")
    root.configure(bg='#000000')

    root.geometry('550x200')
    tk.Label(root, text="Enter the output directory for the generated scripts:\n(Default: system generated scripts)",
             bg='#000000', fg='white',
             font=("Helvetica", 12, 'bold')).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    system_generated_scripts_dir_entry = tk.Entry(root, width=58, bg='#000000', fg='white',
                                                  font=("Helvetica", 12, 'bold'),
                                                  highlightbackground='#007bff', highlightcolor='#007bff',
                                                  highlightthickness=2, insertbackground='white')
    system_generated_scripts_dir_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def run_parser():
        system_generated_scripts_dir = system_generated_scripts_dir_entry.get()
        if not system_generated_scripts_dir:
            root.withdraw()
            response = messagebox.askyesno("Default Directory", "No directory was entered by you.\nDo you want to "
                                                                "generate the scripts in default directory?")
            if response:
                system_generated_scripts_dir = 'system_generated_scripts'
            else:
                messagebox.showerror("Invalid Input", "Please enter a valid directory.")
                root.deiconify()
                return
        root.withdraw()
        run_all_utilities(system_generated_scripts_dir)
        root.destroy()

    def highlight_button():
        nonlocal bg_color
        if bg_color == 'white':
            bg_color = '#007bff'
        else:
            bg_color = 'blue'
        run_button.config(bg=bg_color)
        root.after(500, highlight_button)

    bg_color = 'blue'
    run_button = tk.Button(root, text="Run Parser", command=lambda: run_parser(), bg='#000000', fg='white',
                           font=("Helvetica", 12, 'bold'), relief=tk.FLAT, width=19)
    run_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    root.after(2, highlight_button)

    primary_monitor = get_monitors()[0]
    x = primary_monitor.x + (primary_monitor.width / 4) - (root.winfo_width() / 4)
    y = primary_monitor.y + (primary_monitor.height / 4) - (root.winfo_height() / 4)
    root.geometry(f"+{int(x)}+{int(y)}")

    root.mainloop()


if __name__ == "__main__":
    main()
