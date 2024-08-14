import os
import shutil
import time
from utilities.parser import parser
from utils.utils import get_folder_location

BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[91m'
ORANGE = '\033[38;5;208m'
RESET = '\033[0m'
CYAN = '\033[96m'


def get_base_paths():
    golden_scripts_dir = get_folder_location('golden_scripts')
    system_generated_scripts_dir = get_folder_location('system_generated_scripts')

    if system_generated_scripts_dir is not None and os.path.exists(system_generated_scripts_dir):
        shutil.rmtree(system_generated_scripts_dir)

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    system_generated_scripts_dir = os.path.join(root_dir, 'system_generated_scripts')
    os.makedirs(system_generated_scripts_dir, exist_ok=True)

    return golden_scripts_dir, system_generated_scripts_dir


def run_all_utilities():
    golden_scripts_dir, system_generated_scripts_dir = get_base_paths()
    utilities = [
        (lambda: parser(golden_scripts_dir, system_generated_scripts_dir), "parser"),
    ]

    all_success = True
    start_time = time.time()

    for utility_func, description in utilities:
        print(f"{ORANGE}Running {description}...{RESET}")
        try:
            success = utility_func()
            print(f"{ORANGE}{description} returned: {BOLD}{GREEN}{success}{RESET}")
            if not success:
                print(f"{BOLD}{RED}{description} failed.{RED}{RESET}")
                all_success = False
        except Exception as e:
            print(f"{BOLD}{RED}Exception occurred during {description}: {e}{RESET}")
            all_success = False

    end_time = time.time()
    elapsed_time = end_time - start_time

    if all_success:
        print(f"\n{BOLD}{GREEN}The parser is executed in {CYAN}{elapsed_time:.2f}{RESET} {BOLD}{GREEN}seconds.{RESET}")
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit_code = run_all_utilities()
    exit(exit_code)