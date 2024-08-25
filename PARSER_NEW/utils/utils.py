import os
import json
from conftest import PROJECT_ROOT, RESULTS_DIR, write_file

BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[91m'
ORANGE = '\033[38;5;208m'
RESET = '\033[0m'
CYAN = '\033[96m'


def get_root_path_join(*sub_paths):
    return os.path.join(PROJECT_ROOT, *sub_paths)


def get_file_location(filename):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    for root, dirs, files in os.walk(root_dir):
        if filename in files:
            file_path = os.path.join(root, filename)
            return file_path

    print(f'{RED}File "{filename}" not found in directory "{root_dir}".{RESET}')
    return None


def get_folder_location(folder_name):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    for root, dirs, files in os.walk(root_dir):
        if folder_name in dirs:
            folder_path = os.path.join(root, folder_name)
            return folder_path

    print(f'{RED}Folder "{folder_name}" not found in directory "{root_dir}".{RESET}')
    return None


def get_environment_config(file_path="config.json"):
    try:
        data = read_json(file_path)
        run_only_on = data.get("Run_only_on", "")
        if run_only_on in data.get("environments", {}):
            environment_values = data["environments"][run_only_on]
            print(f"Environment: {run_only_on}")
            return environment_values
        else:
            print(f"Invalid Run_only_on value specified or environment not found: {run_only_on}")
            return None

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return None


def read_json(filename):
    with open(filename, "r") as file:
        try:
            json_data = json.load(file)
            return json_data
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error: Invalid JSON format in file '{filename}': {e}")


def base_url():
    ENVIRONMENT = get_environment_config(r"D:\MyRecentProjects\Data_Utility\database\env_config.json")
    data = read_json(ENVIRONMENT)
    write_file(f"{RESULTS_DIR}\\Allure_Results", "environment.properties", f"ENVIRONMENT = {data.get('Run_only_on')}\n"
                                                                           f"URL: {ENVIRONMENT.get('URL')}\n"
                                                                           f"BOX2: {ENVIRONMENT.get('BOX2')}\n"
                                                                           f"BOX3: {ENVIRONMENT.get('BOX3')}\n"
                                                                           f"BOX4: {ENVIRONMENT.get('BOX4')}\n"
                                                                           f"CPU: {ENVIRONMENT.get('CPU')}\n"
                                                                           f"obs: {ENVIRONMENT.get('obs')}\n")
    return data.get("URL")
