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
            while not getattr(threading.current_thread(), "stop_flag", False):
                try:
                    # Adjusted logic to handle popup visibility with retry
                    popup_locator = page.locator('.el-message-box_message')
                    if popup_locator.is_visible(timeout=1000):
                        page.get_by_role("button", name="OK").click()
                        page.wait_for_timeout(500)  # Shorter wait time
                except Exception as e:
                    # Log the exception if needed
                    pass
                time.sleep(0.5)  # Wait a shorter period before checking again

        # Start the popup handler in a separate thread
        handler_thread = threading.Thread(target=popup_handler, daemon=True)
        handler_thread.start()

        # Execute the main function
        try:
            result = func(page, *args, **kwargs)
        finally:
            # Signal the thread to stop
            handler_thread.stop_flag = True
            handler_thread.join()

        return result

    return wrapper