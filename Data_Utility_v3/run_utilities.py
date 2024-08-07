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


def run_scripts_sequentially(script_paths):
    for script_path in script_paths:
        print(f"Executing: {script_path}")
        exit_code = run_script(script_path)
        if exit_code != 0:
            print(f"Script '{script_path}' failed with exit code {exit_code}.")
            return exit_code
        print(f"Script '{script_path}' executed successfully.")
    print("All scripts executed successfully.")
    return 0


if __name__ == "__main__":
    scripts = [
        "utilities/parser.py",
        "utilities/replacer.py",
    ]


    exit_code = run_scripts_sequentially(scripts)
    if exit_code == 0:
        print("All scripts executed successfully.")
    else:
        print("One or more scripts failed.")
