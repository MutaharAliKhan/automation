import os
import time  # Import the time module
from utilities.parser import parse_scripts, replace_scripts

BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[91m'
ORANGE = '\033[38;5;208m'
RESET = '\033[0m'


def get_base_paths():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir))
    golden_scripts_dir = os.path.join(project_root, 'golden_scripts')
    system_generated_scripts_dir = os.path.join(project_root, 'system_generated_scripts')
    return golden_scripts_dir, system_generated_scripts_dir


def run_all_utilities():
    golden_scripts_dir, system_generated_scripts_dir = get_base_paths()
    utilities = [
        (lambda: parse_scripts(golden_scripts_dir), "parser"),
        (lambda: replace_scripts(system_generated_scripts_dir), "replacer")
    ]

    all_success = True
    start_time = time.time()  # Start timing

    for utility_func, description in utilities:
        print(f"{ORANGE}Running {description}...{RESET}")
        try:
            success = utility_func()
            print(f"{ORANGE}{description} returned: {GREEN}{success}{RESET}")
            if not success:
                print(f"{BOLD}{RED}{description} failed.{RED}{RESET}")
                all_success = False
        except Exception as e:
            print(f"{BOLD}{RED}Exception occurred during {description}: {e}{RESET}")
            all_success = False

    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    print(f"\n{BOLD}{GREEN}All methods executed in {elapsed_time:.2f} seconds.{RESET}")
    if all_success:
        print(f"{BOLD}{GREEN}All methods executed successfully.{RESET}")
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit_code = run_all_utilities()
    exit(exit_code)