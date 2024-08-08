import os
import re

def extract_comments_and_positions(script_path):
    """
    Extract comments and their positions from a Python script.
    """
    comments = []
    with open(script_path, 'r') as file:
        lines = file.readlines()
    
    for i, line in enumerate(lines):
        # Check for comments and their positions
        if line.strip().startswith('#'):
            comments.append((i, line.strip(), len(line) - len(line.lstrip())))
    
    return comments

def insert_comments_with_indentation(script_path, comments):
    """
    Insert comments with proper indentation into the script.
    """
    with open(script_path, 'r') as file:
        lines = file.readlines()
    
    updated_lines = []
    comment_index = 0
    
    for i, line in enumerate(lines):
        if comment_index < len(comments):
            comment_pos, comment_text, comment_indent = comments[comment_index]
            
            if i == comment_pos:
                # Add comment with the correct indentation
                updated_lines.append(f"{' ' * comment_indent}{comment_text}\n")
                comment_index += 1
        
        updated_lines.append(line)
    
    # Ensure any remaining comments are added
    while comment_index < len(comments):
        comment_pos, comment_text, comment_indent = comments[comment_index]
        if i < comment_pos:
            updated_lines.append(f"{' ' * comment_indent}{comment_text}\n")
        comment_index += 1
    
    with open(script_path, 'w') as file:
        file.writelines(updated_lines)

def insert_comments_around_keywords(script_path, comments):
    """
    Insert comments around specific keywords in the script with proper indentation.
    """
    with open(script_path, 'r') as file:
        lines = file.readlines()
    
    updated_lines = []
    comment_iter = iter(comments)
    
    for i, line in enumerate(lines):
        updated_lines.append(line)
        
        if re.search(r'page\.(locator|fill|click)', line):
            try:
                comment_pos, comment_text, comment_indent = next(comment_iter)
                if i == comment_pos:
                    updated_lines.append(f"{' ' * comment_indent}{comment_text}\n")
                else:
                    # Ensure comments are placed above the keyword with the correct indentation
                    if i > comment_pos:
                        updated_lines.append(f"{' ' * comment_indent}{comment_text}\n")
            except StopIteration:
                break
    
    with open(script_path, 'w') as file:
        file.writelines(updated_lines)

def process_scripts(recorded_folder, updated_folder):
    """
    Process scripts from the recorded folder and update corresponding scripts
    in the updated folder with comments.
    """
    for filename in os.listdir(recorded_folder):
        if filename.endswith('.py'):
            recorded_script_path = os.path.join(recorded_folder, filename)
            updated_script_path = os.path.join(updated_folder, filename)
            
            if os.path.exists(updated_script_path):
                # Extract comments and positions from the recorded script
                comments = extract_comments_and_positions(recorded_script_path)
                
                # Update the corresponding script in the updated folder with comments
                insert_comments_around_keywords(updated_script_path, comments)
            else:
                print(f"Updated script {filename} not found in {updated_folder}")

# Define your folder paths here
recorded_folder = 'path_to_recorded_scripts_folder'
updated_folder = 'path_to_updated_scripts_folder'

# Process the scripts
process_scripts(recorded_folder, updated_folder)