import os
import ast

def extract_comments_from_script(script_path):
    """
    Extract comments from a Python script.
    """
    comments = []
    with open(script_path, 'r') as file:
        lines = file.readlines()
    
    for i, line in enumerate(lines):
        if line.strip().startswith('#'):
            comments.append((i, line.strip()))
    
    return comments

def update_script_with_comments(script_path, comments):
    """
    Update a script with comments at the specified lines.
    """
    with open(script_path, 'r') as file:
        lines = file.readlines()
    
    for index, comment in comments:
        if index < len(lines):
            lines[index] = f'{comment}\n' + lines[index]
    
    with open(script_path, 'w') as file:
        file.writelines(lines)

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
                # Extract comments from the recorded script
                comments = extract_comments_from_script(recorded_script_path)
                
                # Update the corresponding script in the updated folder with comments
                update_script_with_comments(updated_script_path, comments)
            else:
                print(f"Updated script {filename} not found in {updated_folder}")

# Define your folder paths here
recorded_folder = 'path_to_recorded_scripts_folder'
updated_folder = 'path_to_updated_scripts_folder'

# Process the scripts
process_scripts(recorded_folder, updated_folder)