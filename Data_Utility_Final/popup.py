from functools import wraps
from threading import Thread
from time import sleep
from playwright.sync_api import Page

def handle_popups_continuously(interval=1):
    """
    Decorator to continuously handle popups in Playwright.
    It runs a background thread that checks for the visibility of a popup at regular intervals,
    validates the message content, and interacts with the popup if it matches expected messages.

    :param interval: Time interval in seconds between each popup check.
    :return: The wrapped function with continuous popup handling.
    """
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            page: Page = kwargs.get('page')
            
            if page is None:
                raise ValueError("The 'page' object must be passed as a keyword argument.")
            
            # Define a flag to control the background thread
            stop_checking = False
            
            def check_popup():
                while not stop_checking:
                    try:
                        # Check if the popup is visible within a short timeout period
                        if page.locator('.el-message-box__message').is_visible(timeout=1000):
                            # Retrieve the message content and convert to lowercase for comparison
                            message = page.locator('.el-message-box__message').text_content().lower()

                            # Define a list of valid messages
                            valid_messages = [
                                "unauthorized financial transactions exist for the selected account. do you want to continue?",
                                "contact compliance department",
                                "sign-on is successful. last sign-on date is",
                                "are you sure you want to sign off?"
                            ]

                            # Assert that the popup message is within the expected valid messages
                            assert message in valid_messages, f"Unexpected pop-up message: {message}"
                            
                            print(f"Pop-up message: {message}")
                            
                            # Click the "OK" button on the popup
                            page.get_by_role("button", name="OK").click()

                            # Optional timeout after the popup interaction
                            page.wait_for_timeout(1000)

                    except TimeoutError:
                        pass
                    
                    sleep(interval)  # Sleep for a short period before checking again

            # Start the popup checking thread
            popup_thread = Thread(target=check_popup)
            popup_thread.start()
            
            # Execute the wrapped function
            try:
                result = func(*args, **kwargs)
            finally:
                # Stop the background thread when the function is done
                stop_checking = True
                popup_thread.join()
            
            return result
        
        return wrapper
    
    return decorator