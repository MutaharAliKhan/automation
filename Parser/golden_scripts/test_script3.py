from playwright.sync_api._generated import Page
from utils.popup_handler import handle_popup


@handle_popup
def test_run(page: Page) -> None:
    page.goto("https://demoqa.com/modal-dialogs")
    page.get_by_role("button", name="Small modal").click()
    page.wait_for_timeout(1000)

