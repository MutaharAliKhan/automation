import os
import pandas as pd
import re
import ast
import astor

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
recorded_scripts_dir = os.path.join(project_root, 'recorded_scripts')
updated_scripts_dir = os.path.join(project_root, 'updated_scripts')
os.makedirs(updated_scripts_dir, exist_ok=True)

script_count = 0
csv_count = 0


def sanitize_name(name: str) -> str:
    name = (name
            .replace("data-e2e", "").replace("data-test", ""))
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    return name


def extract_string_literals(code_line):
    pattern = r"'(?:\\'|[^'])*'|\"(?:\\\"|[^\"])*\""
    matches = re.findall(pattern, code_line)
    strings = [re.sub(r"(^'|'$)|(^\"|\"$)", "", match).replace("\\'", "'").replace('\\"', '"') for match in matches]
    return strings


def find_lines_with_fill(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    results = []
    for line_number, line in enumerate(lines, start=1):
        if 'fill' in line:
            results.append((line_number, line.strip()))
    return results


def extract_fill_data(file):
    fill_data = {}
    column_list = []
    column_count = {}
    result = find_lines_with_fill(file)
    urls = extract_urls(open(file, 'r').read())

    if urls:
        fill_data['url'] = urls[0]

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
    return fill_data


def extract_urls(script_content):
    urls = re.findall(r'page\.goto\(["\']([^"\']+?)["\']\)', script_content)
    return urls


def save_data_to_csv(data, csv_path):
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)


def extract_function_name(script_content):
    match = re.search(r'def (\w+)\(', script_content)
    return match.group(1) if match else 'run'


def read_values_from_csv(csv_path):
    df = pd.read_csv(csv_path)
    values = df.values.tolist()
    return df.columns.tolist(), values


def process_script_with_ast(script_path, updated_script_path, csv_path, script_name):
    with open(script_path, 'r') as file:
        script_content = file.read()

    fill_data = extract_fill_data(script_path)

    save_data_to_csv([fill_data], csv_path)

    tree = ast.parse(script_content)
    static_code = []
    function_name = extract_function_name(script_content)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            func = node.value.func
            if isinstance(func, ast.Attribute):
                if not (func.attr == 'close' and func.value.id in {'browser', 'context'}):
                    static_code.append(astor.to_source(node).strip())

    column_names, csv_data = read_values_from_csv(csv_path)
    param_names = ', '.join(column_names)

    static_code_str = '\n    '.join(static_code)
    updated_script_content = (
        "import pytest\n"
        "import pandas as pd\n"
        "import allure\n"
        "from playwright.sync_api import Page, expect\n\n\n"
        "def read_values_from_csv():\n"
        f"    df = pd.read_csv(r'{csv_path}')\n"
        "    return df.values.tolist()\n\n\n"
        "csv_data = read_values_from_csv()\n\n\n"
        f"@allure.feature('{script_name}')\n"
        f"@allure.story('{script_name}')\n"
        f"@allure.title('{script_name}')\n"
        f"@pytest.mark.parametrize('{param_names}', csv_data)\n"
        f"def test_{function_name}(page: Page, {', '.join(column_names)}) -> None:\n"
        f"    {static_code_str}\n"
    )

    with open(updated_script_path, 'w') as file:
        file.write(updated_script_content)


for script_file in os.listdir(recorded_scripts_dir):
    script_path = os.path.join(recorded_scripts_dir, script_file)

    if os.path.isfile(script_path):
        script_name = os.path.splitext(script_file)[0]
        updated_script_path = os.path.join(updated_scripts_dir, script_file)
        csv_path = os.path.abspath(os.path.join(updated_scripts_dir, f'{script_name}.csv'))

        process_script_with_ast(script_path, updated_script_path, csv_path, script_name)

        script_count += 1
        csv_count += 1

print(f"Scripts have been parsed, updated, and saved successfully.")
print(f"Total scripts updated: {script_count}")
print(f"Total CSV files generated: {csv_count}")
