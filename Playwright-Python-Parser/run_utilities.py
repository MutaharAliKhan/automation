# import subprocess
# import os
# import sys
#
#
# def run_script(script_path):
#     python_executable = r"D:\MyRecentProjects\playwright_parser\venv\Scripts\python.exe"
#     print(f"Using Python executable: {python_executable}")
#     print(f"Attempting to run: {script_path}")
#     try:
#         result = subprocess.run([python_executable, script_path], capture_output=True, text=True)
#         print(f"Running script: {script_path}")
#         print("Output:")
#         print(result.stdout)
#         if result.stderr:
#             print("Errors:")
#             print(result.stderr)
#         return result.returncode
#     except Exception as e:
#         print(f"Failed to run script {script_path}: {e}")
#         return -1
#
#
# if __name__ == "__main__":
#     print(f"Python version: {sys.version}")
#     print(f"Python path: {sys.executable}")
#     print(f"Sys path: {sys.path}")
#
#     script1 = os.path.join("utilities", "parser.py")
#     script2 = os.path.join("utilities", "replacer.py")
#
#     # Check if scripts exist before running
#     for script in [script1, script2]:
#         if not os.path.isfile(script):
#             print(f"Script not found: {script}")
#             exit(1)
#
#     # Run script1
#     print(f"Running {script1}...")
#     exit_code1 = run_script(script1)
#
#     if exit_code1 == 0:
#         print("Script1 executed successfully. Running Script2...")
#         exit_code2 = run_script(script2)
#         if exit_code2 == 0:
#             print("Script2 executed successfully. Running Script3...")
#         else:
#             print("Script2 failed. Script3 will not be executed.")
#     else:
#         print("Script1 failed. Script2 and Script3 will not be executed.")


import subprocess


def run_script(script_path):
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True)
        print(f"Running script: {script_path}")
        print("Output:")
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        return result.returncode
    except Exception as e:
        print(f"Failed to run script {script_path}: {e}")
        return -1


if __name__ == "__main__":
    script1 = "utilities/parser.py"
    script2 = "utilities/replacer.py"

    exit_code1 = run_script(script1)

    if exit_code1 == 0:
        print("Script1 executed successfully. Running Script2...")
        exit_code2 = run_script(script2)
        if exit_code2 == 0:
            print("Script2 executed successfully. Running Script3...")

        else:
            print("Script2 failed. Script3 will not be executed.")
    else:
        print("Script1 failed. Script2 and Script3 will not be executed.")
