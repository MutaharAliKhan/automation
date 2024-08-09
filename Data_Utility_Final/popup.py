from functools import wraps
from playwright.sync_api import Page

def handle_popups(func):
    """
    Decorator to handle popups in Playwright. It checks for the visibility of a popup 
    before and after every significant action in a script, validates the message content, 
    and interacts with the popup if it matches expected messages.
    
    :param func: The original function being decorated.
    :return: The wrapped function with popup handling.
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        page: Page = kwargs.get('page')
        
        if page is None:
            raise ValueError("The 'page' object must be passed as a keyword argument.")
        
        def check_popup():
            try:
                # Check if the popup is visible within the timeout period
                if page.locator('.el-message-box__message').is_visible(timeout=3000):
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
                # If the popup is not visible, continue execution
                pass

        # Check for popup before executing the function
        check_popup()
        
        # Execute the wrapped function
        result = func(*args, **kwargs)
        
        # Check for popup after executing the function
        check_popup()
        
        return result
    
    return wrapper