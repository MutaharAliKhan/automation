import subprocess


BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[91m'
ORANGE = '\033[38;5;208m'  # Orange-like color
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


if __name__ == "__main__":
    scripts = [
        "utilities/parser.py",
        "utilities/replacer.py",
    ]

    exit_code = run_scripts_sequentially(scripts)
    exit(exit_code)
