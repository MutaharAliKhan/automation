import os
import re
import allure
import pytest
from datetime import datetime
from playwright.sync_api import sync_playwright
from allure_commons.types import LinkType
from screeninfo.screeninfo import get_monitors

# Directory setup
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

    # Generate sanitized name for directory
    original_name = request.node.name
    sanitized_name = sanitize_name(original_name)
    iteration_dir = os.path.join(TEST_RESULTS_DIR, f"Iteration-{iteration_count}-{sanitized_name}")
    os.makedirs(iteration_dir, exist_ok=True)
    
    allure.dynamic.link(url=iteration_dir, link_type=LinkType.TEST_CASE, name=iteration_dir)

    # Set up Playwright browser
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

    context.tracing.start(screenshots=True, snapshots=True)

    yield page

    try:
        # Stop tracing and save trace.zip
        trace_path = os.path.join(iteration_dir, 'trace.zip')
        context.tracing.stop(path=trace_path)

        # Capture a screenshot
        screenshot_path = os.path.join(iteration_dir, f"{sanitized_name}_screenshot.png")
        page.screenshot(path=screenshot_path)

        # Create an execution.bat file to open the trace
        execution_bat_path = os.path.join(iteration_dir, 'execution.bat')
        with open(execution_bat_path, 'w') as f:
            f.write(f'playwright show-trace "{trace_path}"\nexit')

    finally:
        page.close()
        context.close()
        browser.close()
        playwright.stop()

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
            allure.attach.file(screenshot_path, name=f"failure-screenshot_{timestamp}", attachment_type=allure.attachment_type.PNG)

# Utility functions
def sanitize_name(name):
    sanitized = re.sub(r'[^a-zA-Z0-9]+', '-', name)
    sanitized = sanitized.strip('-')
    return sanitized.lower()