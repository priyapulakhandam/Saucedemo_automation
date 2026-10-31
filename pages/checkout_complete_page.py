"""Page Object for Checkout: Complete! Page."""

from typing import Tuple
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    """Encapsulates locators and interactions on the order completion page."""

    # Locators
    PAGE_TITLE: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='title']")
    COMPLETE_HEADER: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='complete-header']")
    COMPLETE_TEXT: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='complete-text']")
    BACK_HOME_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='back-to-products']")

    def wait_until_loaded(self) -> "CheckoutCompletePage":
        """Explicitly wait until the order confirmation page is displayed."""
        self.wait_for_url_contains("/checkout-complete.html")
        self.find(self.COMPLETE_HEADER)
        return self

    def get_title_text(self) -> str:
        """Return page title text ('Checkout: Complete!')."""
        return self.get_text(self.PAGE_TITLE)

    def get_confirmation_header(self) -> str:
        """Return the main order confirmation header (e.g. 'Thank you for your order!')."""
        return self.get_text(self.COMPLETE_HEADER)

    def get_confirmation_description(self) -> str:
        """Return the detailed order dispatch description text."""
        return self.get_text(self.COMPLETE_TEXT)

    def click_back_home(self) -> None:
        """Click the Back Home button to return to the inventory catalog."""
        self.js_click(self.BACK_HOME_BUTTON)
        self.wait_for_url_contains("/inventory.html")
