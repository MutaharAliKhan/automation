def extract_comments(script_content):
    comments = {}
    lines = script_content.split('\n')

    in_multiline_comment = False
    multiline_comment_lines = []
    start_delimiter = None

    for index, line in enumerate(lines):
        stripped_line = line.strip()

        if in_multiline_comment:
            multiline_comment_lines.append(stripped_line)
            if stripped_line.endswith(start_delimiter):
                comments[index + 1] = '\n'.join(multiline_comment_lines).strip()
                in_multiline_comment = False
                multiline_comment_lines = []
        elif stripped_line.startswith("'''") or stripped_line.startswith('"""'):
            if stripped_line.endswith("'''") or stripped_line.endswith('"""'):
                # Single-line multiline comment (starts and ends on the same line)
                comments[index + 1] = stripped_line
            else:
                # Start of a multiline comment
                multiline_comment_lines.append(stripped_line)
                in_multiline_comment = True
                start_delimiter = "'''" if stripped_line.startswith("'''") else '"""'
        elif stripped_line.startswith('#'):
            comments[index + 1] = stripped_line

    return comments