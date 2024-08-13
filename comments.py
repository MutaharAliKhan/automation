def extract_comments(script_content):
    comments = {}
    lines = script_content.split('\n')

    in_multiline_comment = False
    multiline_comment_lines = []
    multiline_comment_start = None

    for index, line in enumerate(lines):
        stripped_line = line.strip()

        if in_multiline_comment:
            if stripped_line.endswith("'''") or stripped_line.endswith('"""'):
                multiline_comment_lines.append(stripped_line)
                comments[multiline_comment_start + 1] = '\n'.join(multiline_comment_lines)
                in_multiline_comment = False
                multiline_comment_lines = []
                multiline_comment_start = None
            else:
                multiline_comment_lines.append(stripped_line)
        elif stripped_line.startswith("'''") or stripped_line.startswith('"""'):
            if stripped_line.endswith("'''") or stripped_line.endswith('"""'):
                comments[index + 1] = stripped_line
            else:
                multiline_comment_lines.append(stripped_line)
                in_multiline_comment = True
                multiline_comment_start = index
        elif stripped_line.startswith('#'):
            comments[index + 1] = stripped_line

    return comments