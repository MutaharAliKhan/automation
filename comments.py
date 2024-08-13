def extract_comments(script_content):
    comments = {}
    lines = script_content.split('\n')

    in_multiline_comment = False
    multiline_comment_lines = []
    start_index = 0  # Track the start line number of the multiline comment

    for index, line in enumerate(lines):
        stripped_line = line.strip()

        if in_multiline_comment:
            multiline_comment_lines.append(line)
            if stripped_line.endswith('"""') or stripped_line.endswith("'''"):
                comments[start_index + 1] = '\n'.join(multiline_comment_lines)
                in_multiline_comment = False
                multiline_comment_lines = []
        elif stripped_line.startswith('"""') or stripped_line.startswith("'''"):
            in_multiline_comment = True
            start_index = index
            multiline_comment_lines.append(line)
        elif stripped_line.startswith('#'):
            comments[index + 1] = line

    return comments

# Example usage
if __name__ == "__main__":
    # Reading the content of a Python file
    with open('your_script.py', 'r') as file:
        script_content = file.read()

    # Extract comments from the script content
    comments = extract_comments(script_content)

    # Output the extracted comments
    for line_number, comment in comments.items():
        print(f"Line {line_number}: {comment}")