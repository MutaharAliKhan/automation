import pytest
import os



def run_tests_from_scripts(scripts):
    passed_count = 0
    failed_count = 0

    for script_path in scripts:
        if os.path.exists(script_path):
            print(f"Running tests from {script_path}")
            result = pytest.main([script_path])
            if result == 0:
                print(f"Tests in {script_path} passed.")
                passed_count += 1
            else:
                print(f"Tests in {script_path} failed.")
                failed_count += 1
        else:
            print(f"Script not found: {script_path}")
            failed_count += 1

    return passed_count, failed_count


if __name__ == "__main__":
    test_scripts = [
        "updated_scripts/test_script1.py",
        "updated_scripts/test_script2.py",
        "updated_scripts/test_script3.py",
    ]

    passed, failed = run_tests_from_scripts(test_scripts)


    print(f"\nSummary:")
    print(f"Total Scripts Passed: {passed}")
    print(f"Total Scripts Failed: {failed}")
