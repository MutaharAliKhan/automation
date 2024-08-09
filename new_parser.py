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


def extract_get_by_text(file):
    text_data = {}
    column_list = []
    column_count = {}
    try:
        with open(file, 'r') as f:
            lines = f.readlines()

        for line_number, line in enumerate(lines, start=1):
            if 'get_by_text' in line and '.click()' in line:
                extracted_text = extract_string_literals(line)
                if len(extracted_text) < 1:
                    continue

                column_name = 'text'
                value = sanitize_name(str(extracted_text[0]))

                if column_name in column_count:
                    column_count[column_name] += 1
                    unique_column_name = f"{column_name}{column_count[column_name]}"
                else:
                    column_count[column_name] = 0
                    unique_column_name = column_name

                column_list.append(unique_column_name)
                text_data[unique_column_name] = value
    except Exception as e:
        logging.error(f"Error extracting get_by_text data from {file}: {e}")
    return text_data


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
                column_count[column_name] = 0
                unique_column_name = column_name

            column_list.append(unique_column_name)
            fill_data[unique_column_name] = value

        fill_data.update(text_data)

    except Exception as e:
        logging.error(f"Error extracting fill data from {file}: {e}")
    return fill_data


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
                if function_name.startswith('test_'):
                    function_name = function_name.replace('test_', '')
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
        param_names = ', '.join(column_names) + ', base_url'
        static_code_str = '\n    '.join(static_code)

        db_operations_path = os.path.join(project_root, 'database', 'database_operations.py')
        method_name = f'{script_name}_data'
        if not method_exists(db_operations_path, method_name):
            add_method(db_operations_path, method_name)

        updated_script_content = (
                "import pytest\n"
                "import random\n"
                "import pandas as pd\n"
                "import allure\n"
                "from database.database_operations import *\n"
                "from playwright.sync_api import Page, expect\n\n\n"
                "\n\ntest_data = read_json(r" + "'" + os.path.join(project_root, 'database',
                                                                   'test_data.json') + "'" + ")"
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