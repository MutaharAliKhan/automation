from functools import wraps
from playwright.sync_api import Page

def handle_popups(func):
    """
    Decorator to handle popups in Playwright. It checks for the visibility of a popup, 
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
        
        try:
            # Check if the popup is visible within the timeout period
            if not page.locator('.el-message-box__message').is_visible(timeout=3000):
                raise TimeoutError("Expected pop-up did not appear within the timeout.")
            
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

        except TimeoutError as e:
            # Re-raise the TimeoutError if the popup didn't appear
            raise e

        # Call the original function
        return func(*args, **kwargs)
    
    return wrapper