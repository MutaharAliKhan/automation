import ast
import csv
import re
from collections import defaultdict


def extract_page_lines_and_comments(script_content, exclude_keywords=None):
    tree = ast.parse(script_content)
    page_lines = []
    comment_lines = []
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
            comment_lines.append((lineno, stripped_line))

    return page_lines, comment_lines, excluded_lines


def sanitize_locator(name):
    name = (name.replace("data-e2e", "").replace("data-test", "")
            .replace("input", "").replace("type", ""))
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    return name


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
                func_name = self.get_function_name(node.func)
                if func_name:
                    return f'{func_name}_result'
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

                        if get_text_value:
                            self.add_value_and_locator(get_text_value, get_by_text_var)

                        if fill_value:
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

                    if value_node:
                        locator_str = ast.get_source_segment(script_content, node.func.value.args[0]) if isinstance(
                            locator_node, ast.Call) else ast.get_source_segment(script_content, node.args[0])
                        sanitized_locator = sanitize_locator(locator_str)
                        self.locator_count[sanitized_locator] += 1

                        if self.locator_count[sanitized_locator] > 1:
                            sanitized_locator = f"{sanitized_locator}{self.locator_count[sanitized_locator] - 1}"

                        self.add_value_and_locator(fill_value, sanitized_locator)

                        updated_line = ast.get_source_segment(script_content, node)
                        updated_line = self.replace_string_literal(updated_line, sanitized_locator, fill_value)
                        self.track_updated_line(node, updated_line)

                elif method_name == 'get_by_text':
                    value_node = node.args[0] if node.args else None
                    get_text_value = self.get_string_value(value_node)

                    get_fill_value_var = self._generate_unique_locator('get_text_value')

                    if get_text_value:
                        self.add_value_and_locator(get_text_value, get_fill_value_var)

                        full_line = script_content.splitlines()[node.lineno - 1].strip()
                        updated_line = self.replace_string_literal(full_line, get_fill_value_var, get_text_value)
                        self.track_updated_line(node, updated_line)

                elif method_name == 'filter':
                    has_text_arg = next((kwarg for kwarg in node.keywords if kwarg.arg == 'has_text'), None)
                    if has_text_arg and isinstance(has_text_arg.value, ast.Str):

                        has_text = self.get_string_value(has_text_arg.value)

                        if has_text_arg.value:
                            locator_str = ast.get_source_segment(script_content, node.func.value.args[0]) if isinstance(
                                locator_node, ast.Call) else ast.get_source_segment(script_content, node.args[0])
                            sanitized_locator = sanitize_locator(locator_str)
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


script_path = r'D:\MyRecentProjects\Data_Utility\PARSER\scripting.py'
with open(script_path, 'r') as file:
    script_content = file.read()


page_lines, comments, excluded_lines = extract_page_lines_and_comments(script_content)
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
