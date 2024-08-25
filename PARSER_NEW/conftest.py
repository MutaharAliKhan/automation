import os
import allure
import pytest
from datetime import datetime
from allure_commons.types import LinkType
from screeninfo.screeninfo import get_monitors
from playwright.sync_api._generated import Page

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = None


# """""""""""""""""""""""""""""""""""""""""""""""""Fixtures"""""""""""""""""""""""""""""""""""""""""""""""""
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    global RESULTS_DIR

    try:
        RESULTS_DIR = setup_results_dir()
    except Exception as e:
        print(f"Failed to set up results directory: {e}")
        pytest.exit(f"Exiting due to setup failure: {e}")

    config.option.allure_report_dir = os.path.join(RESULTS_DIR, 'Allure_Results')
    config.option.htmlpath = os.path.join(RESULTS_DIR, 'HTML_Results', 'BasicReport.html')
    config.option.output = os.path.join(RESULTS_DIR, 'Test_Results')


@pytest.fixture(scope='function', autouse=True)
def attach_artifacts_to_allure(request):
    request.addfinalizer(attach_artifact_folder_link_to_allure)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    primary_monitor = get_monitors()[0]
    width = primary_monitor.width - 30
    height = primary_monitor.height - 140
    return {
        **browser_context_args,
        "ignore_https_errors": True,
        "permissions": ['geolocation'],
        "geolocation": {'longitude': 1, 'latitude': 1},
        "viewport": {"width": width, "height": height},
    }


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get('page')
        timestamp = datetime.now().strftime("%d-%m-%Y--%H-%M-%S")
        screenshot_path = os.path.join(get_test_output_dir(), "failure-screenshots",
                                       f"failure-screenshot_{timestamp}.png")
        page.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name=f"failure-screenshot_{timestamp}",
                           attachment_type=allure.attachment_type.PNG)


@pytest.fixture(scope="function")
def page(page: Page):
    return page


@pytest.fixture(scope="function", autouse=True)
def before_test(page):
    yield


@pytest.fixture(scope="function", autouse=True)
def after_test(page):
    yield


@pytest.fixture(scope="session", autouse=True)
def after_all():
    yield


# """""""""""""""""""""""""""""""""""""""""""""""""Functions"""""""""""""""""""""""""""""""""""""""""""""""""
def setup_results_dir():
    global RESULTS_DIR

    base_dir = "D:\\Reports"

    timestamp = datetime.now().strftime("%d-%m-%Y---%I-%M-%S-%p")
    RESULTS_DIR = os.path.join(base_dir, f"Results_{timestamp}")

    allure_results_dir = os.path.join(RESULTS_DIR, "Allure_Results")
    html_results_dir = os.path.join(RESULTS_DIR, "HTML_Results")
    test_results_dir = os.path.join(RESULTS_DIR, "Test_Results")

    try:
        os.makedirs(RESULTS_DIR, exist_ok=True)
        os.makedirs(allure_results_dir, exist_ok=True)
        os.makedirs(html_results_dir, exist_ok=True)
        os.makedirs(test_results_dir, exist_ok=True)
    except Exception as e:
        print(f"Error creating directories: {e}")
        raise

    return RESULTS_DIR


def get_test_result_folder_name():
    folder_name = (os.environ.get('PYTEST_CURRENT_TEST')
                   .replace('::', '-')
                   .replace('/', '-')
                   .replace('--', '-')
                   .replace(" ", "-")
                   .replace('[', '-')
                   .replace(']', '')
                   .replace('_', '-')
                   .replace('.', '-')
                   .replace("-(call)", "")
                   .replace("-(teardown)", "")
                   .replace("-(setup)", "").lower())
    return folder_name


def get_test_output_dir():
    return os.path.join(RESULTS_DIR, "Test_Results", get_test_result_folder_name())


def write_file(directory, name_with_extension, content):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, name_with_extension)
    with open(file_path, 'w') as f:
        f.write(content)


def attach_artifact_folder_link_to_allure():
    write_file(get_test_output_dir(), "execution.bat", "playwright show-trace trace.zip\nexit")
    write_file(RESULTS_DIR, "allure_single_file.bat", "allure generate --single-file Allure_Results\nexit")
    write_file(RESULTS_DIR, "allure_serve.bat", "allure serve Allure_Results")
    allure.dynamic.link(url=get_test_output_dir(), link_type=LinkType.TEST_CASE, name=get_test_output_dir())
