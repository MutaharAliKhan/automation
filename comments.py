def extract_comments(script_content):
    comments = []
    lines = script_content.split('\n')

    in_multiline_comment = False
    multiline_comment_lines = []

    for line in lines:
        stripped_line = line.strip()

        if in_multiline_comment:
            multiline_comment_lines.append(line)  # Preserve original indentation
            if stripped_line.endswith('"""') or stripped_line.endswith("'''"):
                comments.append('\n'.join(multiline_comment_lines))
                in_multiline_comment = False
                multiline_comment_lines = []
        elif stripped_line.startswith('"""') or stripped_line.startswith("'''"):
            in_multiline_comment = True
            multiline_comment_lines.append(line)  # Preserve original indentation
        elif stripped_line.startswith('#'):
            comments.append(line)  # Preserve original indentation

    return comments