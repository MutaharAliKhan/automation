# import subprocess
#
#
# BOLD = '\033[1m'
# GREEN = '\033[92m'
# RED = '\033[91m'
# ORANGE = '\033[38;5;208m'
# RESET = '\033[0m'
#
#
# def run_script(script_path):
#     try:
#         result = subprocess.run(["python", script_path], capture_output=True, text=True)
#         print(f"\n{ORANGE}Executing script: {script_path}{RESET}")
#         print(f"{ORANGE}Output:{RESET}")
#         if result.stdout.strip():
#             print(result.stdout.strip())
#         else:
#             print("No output.")
#         if result.stderr.strip():
#             print(f"{ORANGE}Errors:{RESET}")
#             print(result.stderr.strip())
#         return result.returncode
#     except Exception as e:
#         print(f"{ORANGE}Failed to run script {script_path}: {e}{RESET}")
#         return -1
#
#
# def run_scripts_sequentially(script_paths):
#     all_success = True
#     for script_path in script_paths:
#         exit_code = run_script(script_path)
#         if exit_code != 0:
#             all_success = False
#
#     if all_success:
#         print(f"\n{BOLD}{GREEN}All scripts executed successfully.{RESET}")
#     else:
#         print(f"\n{BOLD}{RED}One or more scripts failed.{RESET}")
#     return 0 if all_success else 1
#
#
# if __name__ == "__main__":
#     scripts = [
#         "utilities/parser.py",
#         "utilities/replacer.py",
#     ]
#
#     exit_code = run_scripts_sequentially(scripts)
#     exit(exit_code)
#
#


import subprocess
import os

from utilities.parser import parse_scripts
from utilities.replacer import replace_scripts

BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[91m'
ORANGE = '\033[38;5;208m'
RESET = '\033[0m'


def run_script(script_path):
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        print(f"\n{ORANGE}Executing script: {script_path}{RESET}")
        print(f"{ORANGE}Output:{RESET}")
        if result.stdout.strip():
            print(result.stdout.strip())
        else:
            print("No output.")
        if result.stderr.strip():
            print(f"{ORANGE}Errors:{RESET}")
            print(result.stderr.strip())
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"{ORANGE}Script execution failed with error: {e}{RESET}")
        return e.returncode
    except Exception as e:
        print(f"{ORANGE}Failed to run script {script_path}: {e}{RESET}")
        return -1


def run_scripts_sequentially(script_paths):
    all_success = True
    for script_path in script_paths:
        exit_code = run_script(script_path)
        if exit_code != 0:
            all_success = False

    if all_success:
        print(f"\n{BOLD}{GREEN}All scripts executed successfully.{RESET}")
    else:
        print(f"\n{BOLD}{RED}One or more scripts failed.{RESET}")
    return 0 if all_success else 1


def get_script_paths(base_dirs):
    def get_py_files(directory):
        return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.py')]

    script_paths = []
    for base_dir in base_dirs:
        script_paths.extend(get_py_files(base_dir))
    return script_paths


def get_base_paths():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    golden_scripts = os.path.join(project_root, 'golden_scripts')
    system_generated_scripts = os.path.join(project_root, 'system_generated_scripts')
    return golden_scripts, system_generated_scripts


if __name__ == "__main__":
    golden_scripts, system_generated_scripts = get_base_paths()
    parse_scripts(golden_scripts, system_generated_scripts)
    replace_scripts(system_generated_scripts)

    script_paths = get_script_paths([golden_scripts, system_generated_scripts])
    exit_code = run_scripts_sequentially(script_paths)

    exit(exit_code)

