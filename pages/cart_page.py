"""Page Object for the SauceDemo Cart Page."""

from typing import List, Tuple, Dict
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from pages.base_page import BasePage


class CartPage(BasePage):
    """Encapsulates locators and interactions on the shopping cart page."""

    # Locators
    PAGE_TITLE: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='title']")
    CART_ITEMS: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    ITEM_NAME: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICE: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    CHECKOUT_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='checkout']")
    CONTINUE_SHOPPING_BUTTON: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='continue-shopping']")

    def wait_until_loaded(self) -> "CartPage":
        """Explicitly wait until cart page and title are displayed."""
        self.wait_for_url_contains("/cart.html")
        self.find(self.PAGE_TITLE)
        return self

    def get_title_text(self) -> str:
        """Return cart page title text ('Your Cart')."""
        return self.get_text(self.PAGE_TITLE)

    def get_cart_item_names(self) -> List[str]:
        """Return the list of all product names present in the cart.

        Uses explicit wait condition resilient to React DOM re-renders.
        """
        def _fetch_names(driver):
            try:
                elements = driver.find_elements(*self.ITEM_NAME)
                if not elements:
                    return False
                return [el.text for el in elements if el.text.strip()]
            except StaleElementReferenceException:
                return False

        return self.wait.until(_fetch_names, message="Cart item names did not load")

    def get_cart_item_prices(self) -> List[str]:
        """Return the list of all product price strings present in the cart.

        Uses explicit wait condition resilient to React DOM re-renders.
        """
        def _fetch_prices(driver):
            try:
                elements = driver.find_elements(*self.ITEM_PRICE)
                if not elements:
                    return False
                return [el.text for el in elements if el.text.strip()]
            except StaleElementReferenceException:
                return False

        return self.wait.until(_fetch_prices, message="Cart item prices did not load")

    def get_cart_items_data(self) -> List[Dict[str, str]]:
        """Return structured list of dicts with name and price for each item."""
        names = self.get_cart_item_names()
        prices = self.get_cart_item_prices()
        return [{"name": n, "price": p} for n, p in zip(names, prices)]

    def click_checkout(self) -> None:
        """Click the Checkout button to proceed to step one."""
        self.js_click(self.CHECKOUT_BUTTON)
        self.wait_for_url_contains("/checkout-step-one.html")
