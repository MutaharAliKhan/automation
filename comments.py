def extract_comments(script_content):
    comments = {}
    lines = script_content.split('\n')

    in_multiline_comment = False
    multiline_comment_lines = []

    for index, line in enumerate(lines):
        stripped_line = line.strip()

        if in_multiline_comment:
            multiline_comment_lines.append(stripped_line)
            if stripped_line.endswith("'''") or stripped_line.endswith('"""'):
                comments[index + 1] = '\n       '.join(multiline_comment_lines)
                in_multiline_comment = False
                multiline_comment_lines = []
        elif stripped_line.startswith("'''") or stripped_line.startswith('"""'):
            multiline_comment_lines.append(stripped_line)
            if not (stripped_line.endswith("'''") or stripped_line.endswith('"""')):
                in_multiline_comment = True
            else:
                comments[index + 1] = stripped_line
        elif '#' in stripped_line:  # Handles both single-line and inline comments
            comment_start = stripped_line.index('#')
            comments[index + 1] = stripped_line[comment_start:].strip()

    return comments