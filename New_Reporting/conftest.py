import os
import re
import json
import allure
import pytest
from datetime import datetime
from allure_commons.types import LinkType
from playwright.sync_api import sync_playwright
from screeninfo.screeninfo import get_monitors

BOLD = '\033[1m'
GREEN = '\033[92m'
RED = '\033[91m'
ORANGE = '\033[38;5;208m'
RESET = '\033[0m'
CYAN = '\033[96m'

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
base_dir = "D:\\Reports"
timestamp = datetime.now().strftime("%d-%m-%Y---%I-%M-%S-%p")
RESULTS_DIR = os.path.join(base_dir, f"Results_{timestamp}")
ALLURE_RESULTS_DIR = os.path.join(RESULTS_DIR, "Allure_Results")
HTML_RESULTS_DIR = os.path.join(RESULTS_DIR, "HTML_Results")
TEST_RESULTS_DIR = os.path.join(RESULTS_DIR, "Test_Results")
iteration_dir = None


@pytest.fixture(scope="session", autouse=True)
def setup_directories():
    os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)
    os.makedirs(HTML_RESULTS_DIR, exist_ok=True)
    os.makedirs(TEST_RESULTS_DIR, exist_ok=True)
    if not hasattr(setup_directories, "iteration_count"):
        setup_directories.iteration_count = 0


@pytest.fixture(scope="function")
def page(request):
    global iteration_dir
    iteration_count = getattr(setup_directories, "iteration_count", 0)
    setup_directories.iteration_count += 1

    original_name = request.node.name
    modified_name = re.sub(r'(\d+)(?!.*\d)', '', original_name)
    request.node.name = modified_name

    iteration_dir = os.path.join(
        TEST_RESULTS_DIR,
        f"Iteration-{iteration_count}-"
        f"{sanitize_name(request.node.name)}"
    )
    os.makedirs(iteration_dir, exist_ok=True)
    allure.dynamic.link(url=iteration_dir, link_type=LinkType.TEST_CASE, name=iteration_dir)

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)

    monitors = get_monitors()
    primary_monitor = monitors[0]
    viewport_width = primary_monitor.width
    viewport_height = primary_monitor.height

    context = browser.new_context(
        ignore_https_errors=True,
        record_video_dir=iteration_dir,
        record_video_size={"width": viewport_width, "height": viewport_height}
    )

    page = context.new_page()
    page.set_viewport_size({"width": viewport_width, "height": viewport_height})

    context.tracing.start(
        screenshots=True,
        snapshots=True
    )

    yield page

    try:
        trace_path = os.path.join(iteration_dir, 'trace.zip')
        context.tracing.stop(path=trace_path)

        screenshot_path = os.path.join(iteration_dir, f"{request.node.name}_screenshot.png")
        page.screenshot(path=screenshot_path)

        execution_bat_path = os.path.join(iteration_dir, 'execution.bat')
        with open(execution_bat_path, 'w') as f:
            f.write(f'playwright show-trace "{trace_path}"\nexit')

    finally:
        page.close()
        context.close()
        browser.close()
        playwright.stop()


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.option.allure_report_dir = os.path.join(RESULTS_DIR, 'Allure_Results')
    config.option.htmlpath = os.path.join(RESULTS_DIR, 'HTML_Results', 'BasicReport.html')


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get('page')
        if page and iteration_dir:
            timestamp = datetime.now().strftime("%d-%m-%Y--%H-%M-%S")
            screenshot_dir = os.path.join(iteration_dir, "failure-screenshot")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"failure-screenshot_{timestamp}.png")
            page.screenshot(path=screenshot_path)
            allure.attach.file(screenshot_path, name=f"failure-screenshot_{timestamp}",
                               attachment_type=allure.attachment_type.PNG)


@pytest.fixture(scope="session", autouse=True)
def before_all():
    yield


@pytest.fixture(scope="function", autouse=True)
def before_test(page):
    yield


@pytest.fixture(scope="function", autouse=True)
def after_test(page):
    write_environment_properties(ALLURE_RESULTS_DIR)
    yield


@pytest.fixture(scope="session", autouse=True)
def after_all():
    attach_batch_files_to_allure()
    yield


def sanitize_name(name):
    sanitized = re.sub(r'[^a-zA-Z0-9]+', '-', name)
    sanitized = sanitized.strip('-')
    return sanitized.lower()


def write_file(directory, name_with_extension, content):
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, name_with_extension)
    with open(file_path, 'w') as f:
        f.write(content)


def attach_batch_files_to_allure():
    write_file(RESULTS_DIR, "allure_single_file.bat", "allure generate --single-file Allure_Results\nexit")
    write_file(RESULTS_DIR, "allure_serve.bat", "allure serve Allure_Results")


def get_environment_config(file_path="config.json"):
    try:
        data = read_json(file_path)
        run_only_on = data.get("Run_only_on", "")
        if run_only_on in data.get("environments", {}):
            environment_values = data["environments"][run_only_on]
            print(f"Environment: {run_only_on}")
            return environment_values, run_only_on
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


def get_file_location(filename):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    for root, dirs, files in os.walk(root_dir):
        if filename in files:
            file_path = os.path.join(root, filename)
            return file_path

    print(f'{RED}File "{filename}" not found in directory "{root_dir}".{RESET}')
    return None


def get_folder_location(folder_name):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    for root, dirs, files in os.walk(root_dir):
        if folder_name in dirs:
            folder_path = os.path.join(root, folder_name)
            return folder_path

    print(f'{RED}Folder "{folder_name}" not found in directory "{root_dir}".{RESET}')
    return None


def write_environment_properties(results_dir):
    env_config_path = get_file_location('env_config.json')
    environment, run_only_on = get_environment_config(env_config_path)
    content = (
        f"ENVIRONMENT = {run_only_on}\n"
        f"URL: {environment.get('URL')}\n"
        f"BOX2: {environment.get('BOX2')}\n"
        f"BOX3: {environment.get('BOX3')}\n"
        f"BOX4: {environment.get('BOX4')}\n"
        f"CPU: {environment.get('CPU')}\n"
        f"OBS: {environment.get('OBS')}\n"
    )
    write_file(os.path.join(results_dir), "environment.properties", content)
