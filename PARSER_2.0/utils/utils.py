import os
import json
import random
import socket
import string
from conftest import PROJECT_ROOT, RESULTS_DIR, write_file, setup_results_dir

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


def get_system_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        print("Error:", e)
        return None


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


def generate_random_cnic():
    five = str(random.randint(10000, 99999))
    seven = str(random.randint(1000000, 9999999))
    one = str(random.randint(0, 9))
    random_cnic = f"{five}-{seven}-{one}"
    return random_cnic


def generate_random_number(minimum, maximum):
    return random.randint(minimum, maximum)


# def _initialize_base_url():
#     global RESULTS_DIR
#     if RESULTS_DIR is None:
#         RESULTS_DIR = setup_results_dir()
#
#     # print(f"{BOLD}{GREEN}Using RESULTS_DIR: {RESULTS_DIR}{RESET}")
#     ENVIRONMENT = get_environment_config(r"D:\MyRecentProjects\Data_Utility\database\env_config.json")
#     write_file(f"{RESULTS_DIR}\\Allure_Results", "environment.properties",
#                f"ENVIRONMENT = {ENVIRONMENT.get('Run_only_on')}\n"
#                f"URL: {ENVIRONMENT.get('URL')}\n"
#                f"BOX2: {ENVIRONMENT.get('BOX2')}\n"
#                f"BOX3: {ENVIRONMENT.get('BOX3')}\n"
#                f"BOX4: {ENVIRONMENT.get('BOX4')}\n"
#                f"CPU: {ENVIRONMENT.get('CPU')}\n"
#                f"obs: {ENVIRONMENT.get('OBS')}\n")
#     return ENVIRONMENT.get("URL")
#
#
# base_url = _initialize_base_url()


def _initialize_base_url():
    global RESULTS_DIR
    if RESULTS_DIR is None:
        if os.path.basename(__file__).startswith("test_"):
            RESULTS_DIR = setup_results_dir()

            ENVIRONMENT = get_environment_config(r"D:\MyRecentProjects\Data_Utility\database\env_config.json")
            write_file(f"{RESULTS_DIR}\\Allure_Results", "environment.properties",
                       f"ENVIRONMENT = {ENVIRONMENT.get('Run_only_on')}\n"
                       f"URL: {ENVIRONMENT.get('URL')}\n"
                       f"BOX2: {ENVIRONMENT.get('BOX2')}\n"
                       f"BOX3: {ENVIRONMENT.get('BOX3')}\n"
                       f"BOX4: {ENVIRONMENT.get('BOX4')}\n"
                       f"CPU: {ENVIRONMENT.get('CPU')}\n"
                       f"obs: {ENVIRONMENT.get('OBS')}\n")

            return ENVIRONMENT.get("URL")


base_url = _initialize_base_url()