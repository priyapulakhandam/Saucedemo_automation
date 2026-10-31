"""Page Object for Checkout Step Two: Overview."""

import re
from typing import Tuple
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutStepTwoPage(BasePage):
    """Encapsulates locators and interactions on the checkout overview page."""

    # Locators
    PAGE_TITLE: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='title']")
    SUBTOTAL_LABEL: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    TAX_LABEL: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='tax-label']")
    TOTAL_LABEL: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='total-label']")
    FINISH_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='finish']")
    CANCEL_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='cancel']")

    def wait_until_loaded(self) -> "CheckoutStepTwoPage":
        """Explicitly wait until the overview page and total elements are displayed."""
        self.wait_for_url_contains("/checkout-step-two.html")
        self.find(self.PAGE_TITLE)
        self.find(self.TOTAL_LABEL)
        return self

    def get_title_text(self) -> str:
        """Return page title text ('Checkout: Overview')."""
        return self.get_text(self.PAGE_TITLE)

    def get_item_total_raw(self) -> str:
        """Return raw string text of the Item total label (e.g. 'Item total: $29.99')."""
        return self.get_text(self.SUBTOTAL_LABEL)

    def get_tax_raw(self) -> str:
        """Return raw string text of the Tax label (e.g. 'Tax: $2.40')."""
        return self.get_text(self.TAX_LABEL)

    def get_total_raw(self) -> str:
        """Return raw string text of the Total label (e.g. 'Total: $32.39')."""
        return self.get_text(self.TOTAL_LABEL)

    @staticmethod
    def _parse_currency(text: str) -> float:
        """Extract float numeric currency amount from a label string."""
        match = re.search(r"[\d]+\.[\d]{2}", text)
        if not match:
            # Fallback for integers or alternate formats
            match = re.search(r"[\d.]+", text)
        if not match:
            raise ValueError(f"Could not parse numeric currency amount from '{text}'")
        return float(match.group())

    def get_item_total_amount(self) -> float:
        """Return parsed float value of item total."""
        return self._parse_currency(self.get_item_total_raw())

    def get_tax_amount(self) -> float:
        """Return parsed float value of tax."""
        return self._parse_currency(self.get_tax_raw())

    def get_total_amount(self) -> float:
        """Return parsed float value of final total."""
        return self._parse_currency(self.get_total_raw())

    def click_finish(self) -> None:
        """Click the Finish button to complete the purchase."""
        self.js_click(self.FINISH_BUTTON)
        self.wait_for_url_contains("/checkout-complete.html")
