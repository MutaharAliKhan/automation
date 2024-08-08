from functools import wraps
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


def handle_popups(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        page: Page = kwargs.get('page')

        try:
            # Check for the pop-up
            if not page.locator('.popup-message').is_visible(timeout=3000):  # Adjust the timeout as needed
                raise PlaywrightTimeoutError("Expected pop-up did not appear within the timeout.")

            message = page.locator('.el-message-box__message').text_content().lower()
            valid_messages = \
                ["Unauthorized financial transactions exist for the selected account. Do you want to continue ?",
                 "contact compliance department", "Transaction has been \"Recorded\"."]

            assert message in valid_messages, f"Unexpected pop-up message: {message}"
            print(f"Pop-up message: {message}")
            page.locator("button[class='el-button el-button--primary']").click()
            page.wait_for_timeout(1000)
        except PlaywrightTimeoutError as e:
            raise e

        return func(*args, **kwargs)

    return wrapper
