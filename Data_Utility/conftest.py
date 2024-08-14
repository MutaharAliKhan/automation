import os
import allure
import pytest
from datetime import datetime
from screeninfo.screeninfo import get_monitors
from utils.utils import RESULTS_DIR, attach_artifact_folder_link_to_allure, get_test_output_dir
from playwright.sync_api._generated import Page
from database.database_connection import get_environment_config


@pytest.fixture(scope='session')
def base_url():
    data = get_environment_config(r"D:\MyRecentProjects\Data_Utility\database\env_config.json")
    return data.get("URL")


@pytest.fixture(scope='session')
def base_url():
    return "https://adactinhotelapp.com/HotelAppBuild2/"


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


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.option.allure_report_dir = os.path.join(RESULTS_DIR, 'Allure_Results')
    config.option.htmlpath = os.path.join(RESULTS_DIR, 'HTML_Results', 'BasicReport.html')
    config.option.output = os.path.join(RESULTS_DIR, 'Test_Results')


@pytest.fixture(scope="function")
def page(page: Page):
    return page


@pytest.fixture(scope="function", autouse=True)
def before_test(page):
    attach_artifact_folder_link_to_allure()
    yield


@pytest.fixture(scope="function", autouse=True)
def after_test(page):
    yield



@pytest.fixture(scope="session", autouse=True)
def after_all():
    yield

