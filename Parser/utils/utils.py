import random
import string
import socket
import os
import allure
from datetime import datetime
from allure_commons.types import LinkType

RESULTS_DIR = ""


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


def get_system_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        print("Error:", e)
        return None


def get_test_result_folder_name():
    folder_name = (os.environ.get('PYTEST_CURRENT_TEST')
                   .replace('::', '-')
                   .replace('/', '-')
                   .replace('--', '-')
                   .replace(" ", "-")
                   .replace(   '[', '-')
                   .replace(']', '')
                   .replace('_', '-')
                   .replace('.', '-')
                   .replace("-(call)", "")
                   .replace("-(setup)","").lower())
    return folder_name


def get_test_output_dir():
    return os.path.join(os.path.join(f"{RESULTS_DIR}\\Test_Results\\", get_test_result_folder_name()))


def write_file(directory, name_with_extension, content):
    folder_path = directory
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_name = name_with_extension
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as f:
        f.write(content)


def attach_artifact_folder_link_to_allure():
    write_file(get_test_output_dir(), "execution.bat", f"playwright show-trace trace.zip\nexit")
    write_file(RESULTS_DIR, "allure_single_file.bat", "allure generate --single-file Allure_Results\nexit")
    write_file(RESULTS_DIR, "allure_serve.bat", "allure serve Allure_Results")
    allure.dynamic.link(url=get_test_output_dir(), link_type=LinkType.TEST_CASE,
                        name=get_test_output_dir())


def create_directories():
    try:
        global RESULTS_DIR
        reports_dir = os.path.join("D:\\", "Reports")
        os.makedirs(reports_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%d-%m-%Y---%I-%M-%S-%p')
        results_dir = os.path.join(reports_dir, f"Results---{timestamp}")
        os.makedirs(results_dir, exist_ok=True)

        return results_dir
    except OSError as e:
        print(f"Error: Failed to create directories - {e}")
        return None


RESULTS_DIR = create_directories()