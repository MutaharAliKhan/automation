import ast
import csv
import re
from collections import defaultdict


def extract_page_lines_and_comments(script_content):
    tree = ast.parse(script_content)
    page_lines = []
    comment_lines = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) or isinstance(node, ast.Assign):
            code_line = ast.get_source_segment(script_content, node)
            if 'page.' in code_line:
                page_lines.append((node.lineno, code_line.strip()))

    for lineno, line in enumerate(script_content.splitlines(), 1):
        stripped_line = line.strip()
        if stripped_line.startswith('#'):
            comment_lines.append((lineno, stripped_line))

    return page_lines, comment_lines


def sanitize_locator(name):
    name = (name.replace("data-e2e", "").replace("data-test", "")
            .replace("input", "").replace("type", ""))
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    return name


def extract_and_replace_fill_values(script_content):
    class FillAndGetByTextVisitor(ast.NodeVisitor):
        def __init__(self):
            self.lines = []
            self.values = []
            self.locators = []
            self.updated_lines = []
            self.locator_count = defaultdict(int)

        def visit_Call(self, node):
            if isinstance(node.func, ast.Attribute):
                method_name = node.func.attr
                locator_node = node.func.value

                if method_name == 'fill' and isinstance(locator_node, ast.Call):
                    if hasattr(locator_node.func, 'attr') and locator_node.func.attr == 'get_by_text':
                        value_node = locator_node.args[0] if locator_node.args else None
                        fill_value_node = node.args[0] if node.args else None
                        if (value_node and isinstance(value_node, ast.Str)) or (
                                fill_value_node and isinstance(fill_value_node, ast.Str)):
                            get_text_value = value_node.s if value_node else None
                            fill_value = fill_value_node.s if fill_value_node else None

                            occurrence_index_text = self.locator_count['get_text_value']
                            get_by_text_var = f'get_text_value{occurrence_index_text}' if occurrence_index_text > 0 else 'get_text_value'
                            self.locator_count['get_text_value'] += 1

                            occurrence_index_fill = self.locator_count['get_fill_value']
                            get_fill_value_var = f'get_fill_value{occurrence_index_fill}' if occurrence_index_fill > 0 else 'get_fill_value'
                            self.locator_count['get_fill_value'] += 1

                            if get_text_value:
                                self.values.append(get_text_value)
                                self.locators.append(get_by_text_var)
                            if fill_value:
                                self.values.append(fill_value)
                                self.locators.append(get_fill_value_var)

                            updated_line = script_content.splitlines()[node.lineno - 1].strip()
                            if get_text_value:
                                updated_line = updated_line.replace(f"'{get_text_value}'", f'str({get_by_text_var})')
                                updated_line = updated_line.replace(f'"{get_text_value}"', f'str({get_by_text_var})')
                            if fill_value:
                                updated_line = updated_line.replace(f"'{fill_value}'", f'str({get_fill_value_var})')
                                updated_line = updated_line.replace(f'"{fill_value}"', f'str({get_fill_value_var})')

                            self.lines.append((node.lineno, updated_line))
                            self.updated_lines.append((node.lineno, updated_line))
                        return

                if method_name == 'fill':
                    value_node = node.args[1] if method_name == 'fill' and len(node.args) == 2 else node.args[
                        0] if node.args else None

                    if value_node and isinstance(value_node, ast.Str):
                        fill_value = value_node.s

                        if isinstance(locator_node, ast.Call):
                            locator_str = ast.get_source_segment(script_content, node.func.value.args[0])
                        else:
                            locator_str = ast.get_source_segment(script_content, node.args[0])

                        sanitized_locator = sanitize_locator(locator_str)
                        self.locator_count[sanitized_locator] += 1

                        if self.locator_count[sanitized_locator] > 1:
                            sanitized_locator = f"{sanitized_locator}{self.locator_count[sanitized_locator] - 1}"

                        self.values.append(fill_value)
                        self.locators.append(sanitized_locator)

                        updated_line = ast.get_source_segment(script_content, node)
                        updated_line = updated_line.replace(f"'{fill_value}'", f'str({sanitized_locator})')
                        updated_line = updated_line.replace(f'"{fill_value}"', f'str({sanitized_locator})')

                        self.lines.append((node.lineno, updated_line))
                        self.updated_lines.append((node.lineno, updated_line))

                elif method_name == 'get_by_text':
                    value_node = node.args[0] if node.args else None
                    if value_node and isinstance(value_node, ast.Str):
                        get_text_value = value_node.s

                        occurrence_index = self.locator_count['get_text_value']
                        variable_name = f'get_text_value{occurrence_index}' if occurrence_index > 0 else 'get_text_value'
                        self.locator_count['get_text_value'] += 1

                        self.values.append(get_text_value)
                        self.locators.append(variable_name)

                        full_line = script_content.splitlines()[node.lineno - 1].strip()
                        updated_line = full_line.replace(f"'{get_text_value}'", f'str({variable_name})')
                        updated_line = updated_line.replace(f'"{get_text_value}"', f'str({variable_name})')

                        self.lines.append((node.lineno, updated_line))
                        self.updated_lines.append((node.lineno, updated_line))

                elif method_name == 'filter':
                    has_text_arg = next((kwarg for kwarg in node.keywords if kwarg.arg == 'has_text'), None)
                    if has_text_arg and isinstance(has_text_arg.value, ast.Str):
                        has_text_value = has_text_arg.value.s

                        occurrence_index = self.locator_count['has_text_value']
                        variable_name = f'has_text_value{occurrence_index}' if occurrence_index > 0 else 'has_text_value'
                        self.locator_count['has_text_value'] += 1

                        self.values.append(has_text_value)
                        self.locators.append(variable_name)

                        full_line = script_content.splitlines()[node.lineno - 1].strip()
                        updated_line = full_line.replace(f"'{has_text_value}'", f'str({variable_name})')
                        updated_line = updated_line.replace(f'"{has_text_value}"', f'str({variable_name})')

                        self.lines.append((node.lineno, updated_line))
                        self.updated_lines.append((node.lineno, updated_line))

                elif isinstance(node.func, ast.Name) and node.func.id == 'randint':
                    if len(node.args) == 2 and all(isinstance(arg, ast.Constant) for arg in node.args):
                        start = node.args[0].value
                        end = node.args[1].value
                        updated_line = script_content.splitlines()[node.lineno - 1].strip()
                        updated_line = updated_line.replace(f'random.randint({start}, {end})', f'str(random.randint({start}, {end}))')
                        self.updated_lines.append((node.lineno, updated_line))
                        return

            self.generic_visit(node)

    tree = ast.parse(script_content)
    visitor = FillAndGetByTextVisitor()
    visitor.visit(tree)

    return visitor.lines, visitor.values, visitor.locators, visitor.updated_lines


def create_csv_file(locators, values, csv_filename='locators_values.csv'):
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


script_path = 'script.py'
with open(script_path, 'r') as file:
    script_content = file.read()

page_lines, comments = extract_page_lines_and_comments(script_content)
lines_with_methods, values, locators, updated_lines = extract_and_replace_fill_values(script_content)

create_csv_file(locators, values)
updated_script = generate_updated_script(page_lines + comments, updated_lines)
params = ', '.join(locators)

updated_script_content = f"""import pytest
import random
from playwright.sync_api import expect
from playwright.sync_api._generated import Page

@pytest.mark.parametrize('{params}', csv_data)
def test_script(page: Page, {params}, base_url) -> None:

    {updated_script}
"""

with open('updated_script.py', 'w') as file:
    file.write(updated_script_content)
