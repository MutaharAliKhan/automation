from abc import ABC, abstractmethod
from playwright.sync_api import sync_playwright, Page

# **Abstraction**: Abstract base class defining a high-level interface for page interactions
class AbstractPage(ABC):
    def __init__(self, page: Page):
        # **Encapsulation**: Private attribute `_page` stores the Playwright Page object
        self._page = page
    
    @abstractmethod
    def navigate(self, url: str):
        """Abstract method to navigate to a URL. Must be implemented by concrete classes."""
        pass

    @abstractmethod
    def fill_input(self, locator: str, value: str):
        """Abstract method to fill an input field. Must be implemented by concrete classes."""
        pass

    @abstractmethod
    def click(self, locator: str):
        """Abstract method to click an element. Must be implemented by concrete classes."""
        pass

# **Inheritance**: Concrete implementation of AbstractPage for the login page
class LoginPage(AbstractPage):
    def __init__(self, page: Page):
        super().__init__(page)  # Inherit constructor from AbstractPage
        # **Encapsulation**: Private attributes for locators
        self._username_input = "input[name='username']"
        self._password_input = "input[name='password']"
        self._login_button = "button[type='submit']"
    
    def navigate(self, url: str):
        """Navigate to the specified URL."""
        self._page.goto(url)
    
    def fill_input(self, locator: str, value: str):
        """Fill the input field identified by the locator."""
        self._page.locator(locator).fill(value)
    
    def click(self, locator: str):
        """Click the element identified by the locator."""
        self._page.locator(locator).click()
    
    def login(self, username: str, password: str):
        """High-level method to perform login."""
        self.fill_input(self._username_input, username)
        self.fill_input(self._password_input, password)
        self.click(self._login_button)

# **Inheritance**: Concrete implementation of AbstractPage for the search page
class SearchPage(AbstractPage):
    def __init__(self, page: Page):
        super().__init__(page)  # Inherit constructor from AbstractPage
        # **Encapsulation**: Private attributes for locators
        self._search_input = "input[name='search']"
        self._search_button = "button[type='search']"
    
    def navigate(self, url: str):
        """Navigate to the specified URL."""
        self._page.goto(url)
    
    def fill_input(self, locator: str, value: str):
        """Fill the search input field identified by the locator."""
        self._page.locator(locator).fill(value)
    
    def click(self, locator: str):
        """Click the search button identified by the locator."""
        self._page.locator(locator).click()
    
    def search(self, query: str):
        """High-level method to perform a search."""
        self.fill_input(self._search_input, query)
        self.click(self._search_button)

# **Polymorphism**: Function demonstrating the use of different page types
def perform_action(page: AbstractPage, action: str, value: str):
    """Perform a specific action on the page based on its type."""
    if isinstance(page, LoginPage):
        if action == "login":
            # Polymorphism: Different pages can handle the action differently
            page.login(value, "default_password")  # Assume a default password for simplicity
    elif isinstance(page, SearchPage):
        if action == "search":
            page.search(value)
    else:
        raise ValueError("Unsupported page type")

# **Encapsulation** and **Inheritance**: Playwright setup and test execution
def main():
    # Set up Playwright
    with sync_playwright() as p:
        # Launch a browser instance
        browser = p.chromium.launch()
        # Open a new page/tab
        page = browser.new_page()
        
        # Instantiate and use LoginPage
        login_page = LoginPage(page)
        login_page.navigate("https://example.com/login")
        perform_action(login_page, "login", "user")
        
        # Instantiate and use SearchPage
        search_page = SearchPage(page)
        search_page.navigate("https://example.com/search")
        perform_action(search_page, "search", "query")
        
        # Close the browser
        browser.close()

if __name__ == "__main__":
    main()








class Calculator:
    
    def add(self, *args):
        """Method to add numbers. Supports variable-length arguments."""
        return sum(args)

# Usage
calc = Calculator()
print(calc.add(1, 2))            # Output: 3
print(calc.add(1, 2, 3, 4))      # Output: 10
print(calc.add(5))               # Output: 5
