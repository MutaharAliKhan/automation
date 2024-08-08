import ast
import astor
import os
import re


class ParamReplacer(ast.NodeTransformer):
    def __init__(self, params):
        self.params = params

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == 'fill':
                if len(node.args) == 2 and isinstance(node.args[1], ast.Str):
                    if self.params:
                        param = self.params.pop(0)
                        node.args[1] = ast.Name(id=param, ctx=ast.Load())
                elif len(node.args) == 1 and isinstance(node.args[0], ast.Str):
                    if self.params:
                        param = self.params.pop(0)
                        node.args[0] = ast.Name(id=param, ctx=ast.Load())
            elif node.func.attr == 'goto':
                node.args[0] = ast.Name(id="base_url", ctx=ast.Load())
        return node


class FillArgumentTransformer(ast.NodeTransformer):
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'fill':
            if len(node.args) > 1:
                if not (isinstance(node.args[1], ast.Call) and isinstance(node.args[1].func, ast.Name) and node.args[1].func.id == 'str'):
                    node.args[1] = ast.Call(func=ast.Name(id='str', ctx=ast.Load()), args=[node.args[1]], keywords=[])
            elif len(node.args) == 1:
                if not (isinstance(node.args[0], ast.Call) and isinstance(node.args[0].func, ast.Name) and node.args[0].func.id == 'str'):
                    node.args[0] = ast.Call(func=ast.Name(id='str', ctx=ast.Load()), args=[node.args[0]], keywords=[])
        return node


def extract_parametrize_params(script_content):
    tree = ast.parse(script_content)
    params = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if (isinstance(node.func.value, ast.Attribute) and
                    isinstance(node.func.value.value, ast.Name) and
                    node.func.value.value.id == 'pytest' and
                    node.func.value.attr == 'mark' and
                    node.func.attr == 'parametrize' and
                    node.args and isinstance(node.args[0], ast.Str)):
                param_names = node.args[0].s.split(', ')
                params.extend(param_names)
    return params


def extract_goto_urls(script_content):
    tree = ast.parse(script_content)
    urls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == 'goto' and len(node.args) == 1 and isinstance(node.args[0], ast.Str):
                urls.append(node.args[0].s)
    return urls


def replace_hardcoded_values_with_params(script_content, params):
    tree = ast.parse(script_content)
    tree = ParamReplacer(params).visit(tree)
    return astor.to_source(tree)


def extract_comments(script_content):
    comments = {}
    lines = script_content.splitlines(keepends=True)

    in_multiline_comment = False
    multiline_comment_lines = []

    for index, line in enumerate(lines):
        stripped_line = line.strip()

        if in_multiline_comment:
            multiline_comment_lines.append(line)
            if stripped_line.endswith("'''") or stripped_line.endswith('"""'):
                comments[index] = ''.join(multiline_comment_lines)
                in_multiline_comment = False
                multiline_comment_lines = []
        elif stripped_line.startswith("'''") or stripped_line.startswith('"""'):
            if stripped_line.endswith("'''") or stripped_line.endswith('"""'):
                comments[index] = line
            else:
                multiline_comment_lines.append(line)
                in_multiline_comment = True
        elif stripped_line.startswith('#'):
            comments[index] = line

    return comments


def reinsert_comments(script_content, comments):
    lines = script_content.splitlines(keepends=True)
    comment_lines = [lines[idx] for idx in sorted(comments.keys())]

    # Create a new list of lines with comments reinserted
    new_lines = []
    comment_index = 0

    for i, line in enumerate(lines):
        if comment_index < len(comment_lines) and i == sorted(comments.keys())[comment_index]:
            new_lines.append(comment_lines[comment_index])
            comment_index += 1
        new_lines.append(line)

    # Add any remaining comments (in case there are more comments than lines)
    while comment_index < len(comment_lines):
        new_lines.append(comment_lines[comment_index])
        comment_index += 1

    return ''.join(new_lines)


def transform_fill_arguments(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()

        tree = ast.parse(code)
        transformer = FillArgumentTransformer()
        tree = transformer.visit(tree)
        updated_code = astor.to_source(tree)

        with open(file_path, 'w') as file:
            file.write(updated_code)

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def process_script(file_path):
    try:
        with open(file_path, 'r') as file:
            script_content = file.read()

        # Extract comments before transformations
        comments = extract_comments(script_content)
        
        # Extract parameters and URLs
        params = extract_parametrize_params(script_content)
        urls = extract_goto_urls(script_content)

        if urls:
            params.append('url')

        # Replace hardcoded values with parameters
        if params:
            updated_script_content = replace_hardcoded_values_with_params(script_content, params.copy())
            
            # Reinsert comments into the updated script
            updated_script_content = reinsert_comments(updated_script_content, comments)
            
            with open(file_path, 'w') as file:
                file.write(updated_script_content)

        # Transform fill arguments
        if transform_fill_arguments(file_path):
            return True
        return False

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def process_directory(dir_path):
    count = 0
    for root, _, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if process_script(file_path):
                    count += 1

    print(f"Total updated scripts count: {count}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    directory_path = os.path.join(project_root, 'updated_scripts')
    process_directory(directory_path)
