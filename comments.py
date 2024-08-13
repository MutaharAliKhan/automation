def extract_comments(script_content):
    comments = {}
    lines = script_content.split('\n')

    in_multiline_comment = False
    multiline_comment_lines = []
    comment_type = None  # 'single' for #, 'triple_single' for '''...''', 'triple_double' for """..."""

    for index, line in enumerate(lines):
        stripped_line = line.strip()

        if in_multiline_comment:
            if comment_type == 'triple_single' and stripped_line.endswith("'''"):
                multiline_comment_lines.append(stripped_line)
                comments[index + 1] = '\n       '.join(multiline_comment_lines)
                in_multiline_comment = False
                multiline_comment_lines = []
            elif comment_type == 'triple_double' and stripped_line.endswith('"""'):
                multiline_comment_lines.append(stripped_line)
                comments[index + 1] = '\n       '.join(multiline_comment_lines)
                in_multiline_comment = False
                multiline_comment_lines = []
            else:
                multiline_comment_lines.append(stripped_line)
        elif stripped_line.startswith("'''"):
            if stripped_line.endswith("'''"):
                comments[index + 1] = stripped_line
            else:
                multiline_comment_lines.append(stripped_line)
                in_multiline_comment = True
                comment_type = 'triple_single'
        elif stripped_line.startswith('"""'):
            if stripped_line.endswith('"""'):
                comments[index + 1] = stripped_line
            else:
                multiline_comment_lines.append(stripped_line)
                in_multiline_comment = True
                comment_type = 'triple_double'
        elif stripped_line.startswith('#'):
            comments[index + 1] = stripped_line

    return comments