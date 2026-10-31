"""Page Object for Checkout Step One: Your Information."""

from typing import Tuple
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    """Encapsulates locators and interactions on the first checkout step."""

    # Locators
    PAGE_TITLE: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='title']")
    FIRST_NAME_INPUT: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME_INPUT: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE_INPUT: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='continue']")
    CANCEL_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='cancel']")
    ERROR_CONTAINER: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='error']")

    def wait_until_loaded(self) -> "CheckoutStepOnePage":
        """Explicitly wait until the step one page is loaded."""
        self.wait_for_url_contains("/checkout-step-one.html")
        self.find(self.FIRST_NAME_INPUT)
        return self

    def enter_first_name(self, first_name: str) -> "CheckoutStepOnePage":
        """Fill in the First Name input."""
        self.type_text(self.FIRST_NAME_INPUT, first_name)
        return self

    def enter_last_name(self, last_name: str) -> "CheckoutStepOnePage":
        """Fill in the Last Name input."""
        self.type_text(self.LAST_NAME_INPUT, last_name)
        return self

    def enter_postal_code(self, postal_code: str) -> "CheckoutStepOnePage":
        """Fill in the Zip / Postal Code input."""
        self.type_text(self.POSTAL_CODE_INPUT, postal_code)
        return self

    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> "CheckoutStepOnePage":
        """Convenience method to fill the full customer information form."""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self

    def click_continue(self) -> None:
        """Click the Continue button to advance to overview step or trigger validation."""
        self.js_click(self.CONTINUE_BUTTON)

    def submit_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        """Fill details and click continue."""
        self.fill_information(first_name, last_name, postal_code)
        self.click_continue()

    def get_error_message(self) -> str:
        """Return the validation error message text."""
        return self.get_text(self.ERROR_CONTAINER)

    def is_error_displayed(self) -> bool:
        """Check if error message container is visible."""
        return self.is_displayed(self.ERROR_CONTAINER, timeout=5)
