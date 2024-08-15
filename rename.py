import os

def rename_scripts(directory):
    try:
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.py') and not filename.startswith('test_'):
                    new_filename = f'test_{filename}'
                    old_path = os.path.join(root, filename)
                    new_path = os.path.join(root, new_filename)
                    os.rename(old_path, new_path)
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False