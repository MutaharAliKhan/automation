import functools
import threading
import time
from playwright.sync_api import Page

def handle_popups(func):
    """
    A decorator that handles popups during the execution of the decorated function.

    This decorator starts a separate thread that continuously checks for and handles popups
    by clicking on a button identified by the selector '#okbutton'. The thread is stopped 
    once the decorated function has completed execution.

    Args:
        func (function): The function to be decorated.

    Returns:
        wrapper (function): The wrapped function that includes popup handling.
    """

    @functools.wraps(func)
    def wrapper(page: Page, *args, **kwargs):
        def popup_handler():
            while not getattr(threading.current_thread(), "stop_flag", False):
                try:
                    locator = page.locator('#okbutton')
                    if locator.is_visible():
                        locator.click()
                        # Ensure that the click action is processed
                        page.wait_for_timeout(500)
                except Exception as e:
                    # Optionally log or handle the exception
                    print(f"Popup handling error: {e}")
                time.sleep(0.5)

        # Create and start the thread for handling popups
        handler_thread = threading.Thread(target=popup_handler, daemon=True)
        handler_thread.start()

        try:
            # Execute the decorated function
            result = func(page, *args, **kwargs)
        finally:
            # Signal the thread to stop and wait for it to finish
            setattr(threading.current_thread(), "stop_flag", True)
            handler_thread.join()

        return result

    return wrapper