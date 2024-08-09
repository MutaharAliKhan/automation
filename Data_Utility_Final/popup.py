from functools import wraps
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import threading

def handle_popups(func):
    """
    Decorator to handle popups in Playwright. It continuously checks for the visibility of a popup,
    validates the message content, and interacts with the popup if it matches expected messages.
    
    :param func: The original function being decorated.
    :return: The wrapped function with popup handling.
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        page: Page = kwargs.get('page')
        
        if page is None:
            raise ValueError("The 'page' object must be passed as a keyword argument.")
        
        stop_thread = False

        def check_and_handle_popup():
            """Function to check and handle popup if it appears."""
            valid_messages = [
                "unauthorized financial transactions exist for the selected account. do you want to continue?",
                "contact compliance department",
                "sign-on is successful. last sign-on date is",
                "are you sure you want to sign off?"
            ]

            while not stop_thread:
                try:
                    popup_locator = page.locator('.el-message-box__message')
                    if popup_locator.is_visible(timeout=1000):  # Check with a short timeout
                        message = popup_locator.text_content().strip().lower()

                        if message in valid_messages:
                            print(f"Pop-up message: {message}")
                            page.get_by_role("button", name="OK").click()
                            page.wait_for_timeout(1000)  # Wait a bit after clicking OK
                        else:
                            print(f"Unexpected pop-up message: {message}")
                    else:
                        page.wait_for_timeout(500)  # Short delay before checking again

                except PlaywrightTimeoutError:
                    continue  # No popup appeared within the short timeout
                except Exception as e:
                    print(f"An error occurred while handling the pop-up: {str(e)}")

        # Run the popup checker in a separate thread
        popup_thread = threading.Thread(target=check_and_handle_popup)
        popup_thread.start()

        try:
            # Run the original function
            result = func(*args, **kwargs)
        finally:
            # Stop the popup checking thread
            stop_thread = True
            popup_thread.join()

        return result
    
    return wrapper