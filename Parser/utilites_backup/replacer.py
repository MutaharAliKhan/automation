# import csv
# import os
# import re
#
#
# def get_csv_headers(file_path):
#     with open(file_path, mode='r', newline='') as csvfile:
#         reader = csv.reader(csvfile)
#         headers = next(reader)
#     return headers
#
#
# def replace_arguments(file_path, headers):
#     with open(file_path, 'r') as file:
#         code = file.read()
#
#     fill_pattern = re.compile(r'\.fill\(([^)]+)\)', re.DOTALL)
#     click_pattern = re.compile(r"page\.get_by_text\(([^)]+)\)", re.DOTALL)
#     header_index = 0
#
#     def replace_fill(match):
#         nonlocal header_index
#
#         args = match.group(1).strip()
#
#         if 'random.randint' in args and not 'str(random.randint' in args:
#             return re.sub(r'random\.randint\(([^,]+), ([^)]+)\)', r'str(random.randint(\1, \2))', match.group(0))
#
#
#         if 'str(' in args:
#             return match.group(0)
#
#         if header_index >= len(headers):
#             return match.group(0)
#
#         if ',' in args:
#             first_arg, second_arg = args.split(',', 1)
#             new_second_arg = f'str({headers[header_index]})'
#             header_index += 1
#             return f'.fill({first_arg.strip()}, {new_second_arg})'
#         else:
#             new_arg = f'str({headers[header_index]})'
#             header_index += 1
#             return f'.fill({new_arg})'
#
#     def replace_click(match):
#         nonlocal header_index
#
#         args = match.group(1).strip()
#
#         if 'str(' in args:
#             return match.group(0)
#
#         if header_index >= len(headers):
#             return match.group(0)
#
#         new_arg = f'str({headers[header_index]})'
#         header_index += 1
#         return f'page.get_by_text({new_arg})'
#
#     updated_code = fill_pattern.sub(replace_fill, code)
#     updated_code = click_pattern.sub(replace_click, updated_code)
#
#     with open(file_path, 'w') as file:
#         file.write(updated_code)
#
#
# def find_csv_base_names(directory):
#     csv_base_names = []
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.csv'):
#                 base_name = os.path.splitext(file)[0]
#                 csv_base_names.append(base_name)
#     return csv_base_names
#
#
# def replace_goto_calls(file_path):
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
#     code = ''.join(lines)
#     goto_pattern = re.compile(r'page\.goto\((.*?)\)', re.DOTALL)
#     updated_code = goto_pattern.sub(f'page.goto(base_url)', code)
#     with open(file_path, 'w') as file:
#         file.write(updated_code)
#
#
# def run_replace_all():
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     project_root = os.path.abspath(os.path.join(script_dir, '..'))
#     directory_path = os.path.join(project_root, 'system_generated_scripts')
#     csv_base_names = find_csv_base_names(directory_path)
#
#     updated_scripts_count = 0
#
#     for base_name in csv_base_names:
#         csv_file_path = os.path.join(directory_path, f'{base_name}.csv')
#         python_file_path = os.path.join(directory_path, f'{base_name}.py')
#         headers = get_csv_headers(csv_file_path)
#
#         replace_arguments(python_file_path, headers)
#         replace_goto_calls(python_file_path)
#
#         updated_scripts_count += 1
#
#     print(f"Total updated scripts count: {updated_scripts_count}")
#
#
# run_replace_all()

######################################################################################################################

import csv
import os
import re


def get_csv_headers(file_path):
    with open(file_path, mode='r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
    return headers


def replace_arguments(file_path, headers):
    with open(file_path, 'r') as file:
        code = file.read()

    fill_pattern = re.compile(r'\.fill\(([^)]+)\)', re.DOTALL)
    click_pattern = re.compile(r"page\.get_by_text\(([^)]+)\)", re.DOTALL)
    header_index = 0

    def replace_fill(match):
        nonlocal header_index

        args = match.group(1).strip()

        if 'random.randint' in args and not 'str(random.randint' in args:
            return re.sub(r'random\.randint\(([^,]+), ([^)]+)\)', r'str(random.randint(\1, \2))', match.group(0))

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


def find_csv_base_names(directory):
    csv_base_names = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                base_name = os.path.splitext(file)[0]
                csv_base_names.append(base_name)
    return csv_base_names


def replace_goto_calls(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    code = ''.join(lines)
    goto_pattern = re.compile(r'page\.goto\((.*?)\)', re.DOTALL)
    updated_code = goto_pattern.sub(f'page.goto(base_url)', code)
    with open(file_path, 'w') as file:
        file.write(updated_code)


def rename_scripts(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.py') and not filename.startswith('test_'):
            new_filename = 'test_' + filename
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            os.rename(old_path, new_path)


def run_replace_all():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    directory_path = os.path.join(project_root, 'system_generated_scripts')
    csv_base_names = find_csv_base_names(directory_path)

    updated_scripts_count = 0

    for base_name in csv_base_names:
        csv_file_path = os.path.join(directory_path, f'{base_name}.csv')
        python_file_path = os.path.join(directory_path, f'{base_name}.py')
        headers = get_csv_headers(csv_file_path)

        replace_arguments(python_file_path, headers)
        replace_goto_calls(python_file_path)

        updated_scripts_count += 1

    print(f"Total updated scripts count: {updated_scripts_count}")

    rename_scripts(directory_path)
    print("Scripts renamed to include 'test_' prefix if not already present.")


run_replace_all()

