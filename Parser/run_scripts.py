import pytest
import os

RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[32m"
RED = "\033[31m"
ORANGE = "\033[33m"
CYAN = "\033[36m"

def run_tests_from_scripts(scripts):
    passed_count = 0
    failed_count = 0

    for script_path in scripts:
        if os.path.exists(script_path):
            print(f"Running tests from {script_path}")
            result = pytest.main([script_path])
            if result == 0:
                print(f"{BOLD}{GREEN}Tests in {script_path} passed.{RESET}")
                passed_count += 1
            else:
                print(f"{BOLD}{RED}Tests in {script_path} failed.{RESET}")
                failed_count += 1
        else:
            print(f"{BOLD}{RED}Script not found: {script_path}{RESET}")
            failed_count += 1

    return passed_count, failed_count


if __name__ == "__main__":
    test_scripts = [
        "system_generated_scripts/test_script4.py",
    ]

    passed, failed = run_tests_from_scripts(test_scripts)
    print(f"\n{BOLD}{ORANGE}Summary:{RESET}")
    print(f"{BOLD}{CYAN}-----------------------------{RESET}")
    print(f"{BOLD}Total Scripts {GREEN}Passed:{RESET} {BOLD}{GREEN}{passed}{RESET}")
    print(f"{BOLD}Total Scripts {RED}Failed:{RESET} {BOLD}{RED}{failed}{RESET}")
    print(f"{BOLD}{CYAN}-----------------------------{RESET}")
