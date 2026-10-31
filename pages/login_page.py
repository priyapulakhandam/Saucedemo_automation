"""Page Object for the SauceDemo Login Page."""

from typing import Tuple
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Encapsulates locators and user interactions on the login page."""

    # Locators
    USERNAME_INPUT: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='username']")
    PASSWORD_INPUT: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='password']")
    LOGIN_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='login-button']")
    ERROR_CONTAINER: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='error']")

    def load(self) -> "LoginPage":
        """Navigate to the SauceDemo login page."""
        self.open("")
        self.find(self.USERNAME_INPUT)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        """Enter username into the username field."""
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        """Enter password into the password field."""
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        """Click the Login button."""
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        """Perform full login flow with given credentials."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self) -> str:
        """Retrieve the exact text of the validation/login error message."""
        return self.get_text(self.ERROR_CONTAINER)

    def is_error_displayed(self) -> bool:
        """Check if an error banner is displayed on the page."""
        return self.is_displayed(self.ERROR_CONTAINER)
