def extract_comments(script_content):
    comments = {}
    lines = script_content.split('\n')

    in_multiline_comment = False
    multiline_comment_lines = []

    for index, line in enumerate(lines):
        stripped_line = line.strip()

        if in_multiline_comment:
            if stripped_line.endswith("'''") or stripped_line.endswith('"""'):
                multiline_comment_lines.append(line)
                # Join all multiline comment lines exactly as they are
                comments[index + 1] = '\n'.join(multiline_comment_lines).strip()
                in_multiline_comment = False
                multiline_comment_lines = []
            else:
                multiline_comment_lines.append(line)
        elif stripped_line.startswith("'''") or stripped_line.startswith('"""'):
            if stripped_line.endswith("'''") or stripped_line.endswith('"""'):
                comments[index + 1] = line
            else:
                multiline_comment_lines.append(line)
                in_multiline_comment = True
        elif stripped_line.startswith('#'):
            comments[index + 1] = line

    return comments





def extract_comments(script_content):
    comments = {}
    lines = script_content.split('\n')

    in_multiline_comment = False
    multiline_comment_lines = []

    for index, line in enumerate(lines):
        stripped_line = line.strip()

        if in_multiline_comment:
            multiline_comment_lines.append(line)
            if stripped_line.endswith('"""') or stripped_line.endswith("'''"):
                comments[index + 1] = '\n'.join(multiline_comment_lines)
                in_multiline_comment = False
                multiline_comment_lines = []
        elif stripped_line.startswith('"""') or stripped_line.startswith("'''"):
            in_multiline_comment = True
            multiline_comment_lines.append(line)
        elif stripped_line.startswith('#'):
            comments[index + 1] = line

    return comments