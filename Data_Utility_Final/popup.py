from functools import wraps
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
import time

def handle_popups(func):
    """
    Decorator to handle popups in Playwright. It continuously checks for the visibility of a popup,
    validates the message content, and interacts with the popup if it matches expected messages.
    
    :param func: The original function being decorated.
    :return: The wrapped function with popup handling.
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Retrieve the 'page' object from kwargs, or raise an error if it's not provided
        page: Page = kwargs.get('page')
        
        if page is None:
            raise ValueError("The 'page' object must be passed as a keyword argument.")
        
        def check_and_handle_popup():
            """Function to check and handle popup if it appears."""
            try:
                popup_locator = page.locator('.el-message-box__message')
                if popup_locator.is_visible(timeout=1000):  # Check with a shorter timeout
                    message = popup_locator.text_content().strip().lower()

                    valid_messages = [
                        "unauthorized financial transactions exist for the selected account. do you want to continue?",
                        "contact compliance department",
                        "sign-on is successful. last sign-on date is",
                        "are you sure you want to sign off?"
                    ]

                    if message in valid_messages:
                        print(f"Pop-up message: {message}")
                        page.get_by_role("button", name="OK").click()
                        page.wait_for_timeout(1000)
                    else:
                        print(f"Unexpected pop-up message: {message}")
            except PlaywrightTimeoutError:
                pass  # No popup appeared within the short timeout
            except Exception as e:
                print(f"An error occurred while handling the pop-up: {str(e)}")
        
        # Run the function in a loop to continuously check for popups
        result = None
        try:
            while True:
                start_time = time.time()
                
                # Run the original function and check for popups periodically
                result = func(*args, **kwargs)
                
                # Check for a popup after a short interval
                check_and_handle_popup()
                
                # Break out of the loop if the function completes successfully
                if time.time() - start_time > 10:  # Adjust this value if needed
                    break

        except Exception as e:
            print(f"Exception in the main function: {str(e)}")
            raise
        
        return result
    
    return wrapper
