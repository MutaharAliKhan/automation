def extract_comments(script_content):
    comments = []
    lines = script_content.split('\n')

    in_multiline_comment = False
    multiline_comment_lines = []

    for line in lines:
        stripped_line = line.strip()

        if in_multiline_comment:
            if stripped_line.endswith('"""') or stripped_line.endswith("'''"):
                multiline_comment_lines.append(line)  # Add the ending line with original indentation
                comments.append('\n'.join(multiline_comment_lines))
                in_multiline_comment = False
                multiline_comment_lines = []
            else:
                multiline_comment_lines.append(line)
        elif stripped_line.startswith('"""') or stripped_line.startswith("'''"):
            multiline_comment_lines.append(line)  # Add the starting line with original indentation
            if stripped_line.endswith('"""') or stripped_line.endswith("'''"):
                comments.append('\n'.join(multiline_comment_lines))
                multiline_comment_lines = []
            else:
                in_multiline_comment = True
        elif stripped_line.startswith('#') and not stripped_line.lstrip('#').strip().startswith('-'):
            comments.append(line)

    return comments