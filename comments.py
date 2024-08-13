def extract_comments(script_content):
    comments = []
    lines = script_content.split('\n')

    in_multiline_comment = False
    multiline_comment_lines = []
    comment_type = None  # 'triple_single' for '''...''', 'triple_double' for """..."""

    for line in lines:
        stripped_line = line.strip()

        if in_multiline_comment:
            if comment_type == 'triple_single' and stripped_line.endswith("'''"):
                multiline_comment_lines.append(line)  # Keep original formatting
                comments.append('\n'.join(multiline_comment_lines))
                in_multiline_comment = False
                multiline_comment_lines = []
            elif comment_type == 'triple_double' and stripped_line.endswith('"""'):
                multiline_comment_lines.append(line)  # Keep original formatting
                comments.append('\n'.join(multiline_comment_lines))
                in_multiline_comment = False
                multiline_comment_lines = []
            else:
                multiline_comment_lines.append(line)  # Keep original formatting
        elif stripped_line.startswith("'''"):
            if stripped_line.endswith("'''"):
                comments.append(line)  # Keep original formatting
            else:
                multiline_comment_lines.append(line)  # Keep original formatting
                in_multiline_comment = True
                comment_type = 'triple_single'
        elif stripped_line.startswith('"""'):
            if stripped_line.endswith('"""'):
                comments.append(line)  # Keep original formatting
            else:
                multiline_comment_lines.append(line)  # Keep original formatting
                in_multiline_comment = True
                comment_type = 'triple_double'
        elif stripped_line.startswith('#'):
            comments.append(line)  # Keep original formatting

    return comments