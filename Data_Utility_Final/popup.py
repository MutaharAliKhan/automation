import functools
import threading
import time
from playwright.sync_api import Page

def handle_popups(func):
    """
    A decorator to handle popups during test execution. This decorator continuously 
    checks for and handles popups while the wrapped function is executing.

    Args:
        func (function): The function to be decorated.
    """
    @functools.wraps(func)
    def wrapper(page: Page, *args, **kwargs):
        # Function to continuously check for and handle popups
        def popup_handler():
            while True:
                try:
                    if page.locator('.el-message-box_message').is_visible(timeout=3000):
                        page.get_by_role("button", name="OK").click()
                        page.wait_for_timeout(1868)
                except Exception:
                    pass
                time.sleep(1)  # Wait for a short period before checking again

        # Start the popup handler in a separate thread
        handler_thread = threading.Thread(target=popup_handler, daemon=True)
        handler_thread.start()

        # Execute the main function
        result = func(page, *args, **kwargs)

        # Optionally, you can wait for the popup handler to finish
        # (depends on your specific needs and whether you need to ensure all popups are handled before finishing)
        handler_thread.join()

        return result

    return wrapper