"""Page Object for the SauceDemo Inventory (Products) Page."""

from typing import List, Tuple, Dict
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Encapsulates locators and interactions on the inventory/products page."""

    # Locators
    PAGE_TITLE: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='title']")
    INVENTORY_ITEMS: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    ITEM_NAME: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICE: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    SHOPPING_CART_LINK: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    SHOPPING_CART_BADGE: Tuple[str, str] = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")

    def wait_until_loaded(self) -> "InventoryPage":
        """Explicitly wait until the inventory page and products title are visible."""
        self.wait_for_url_contains("/inventory.html")
        self.find(self.PAGE_TITLE)
        return self

    def get_title_text(self) -> str:
        """Return the text of the main products page title ('Products')."""
        return self.get_text(self.PAGE_TITLE)

    def get_all_items(self):
        """Return all inventory item card elements."""
        return self.find_all(self.INVENTORY_ITEMS)

    def get_product_details_by_index(self, index: int) -> Dict[str, str]:
        """Retrieve the name and price of a product by zero-based index."""
        def _get_details(driver):
            try:
                items = driver.find_elements(*self.INVENTORY_ITEMS)
                if len(items) <= index:
                    return False
                item = items[index]
                name = item.find_element(*self.ITEM_NAME).text
                price = item.find_element(*self.ITEM_PRICE).text
                return {"name": name, "price": price}
            except StaleElementReferenceException:
                return False

        return self.wait.until(_get_details, message=f"Could not read product details for index {index}")

    def add_product_to_cart_by_index(self, index: int) -> Dict[str, str]:
        """Click the Add to Cart button for the item at the given index.

        Returns a dictionary with 'name' and 'price' of the added product.
        """
        def _add_item(driver):
            try:
                items = driver.find_elements(*self.INVENTORY_ITEMS)
                if len(items) <= index:
                    return False
                item = items[index]
                name = item.find_element(*self.ITEM_NAME).text
                price = item.find_element(*self.ITEM_PRICE).text
                btn = item.find_element(By.TAG_NAME, "button")
                driver.execute_script("arguments[0].click();", btn)
                return {"name": name, "price": price}
            except StaleElementReferenceException:
                return False

        return self.wait.until(_add_item, message=f"Could not add product at index {index} to cart")

    def add_product_to_cart_by_name(self, product_name: str) -> Dict[str, str]:
        """Find a product by its name and click its Add to Cart button."""
        def _add_by_name(driver):
            try:
                items = driver.find_elements(*self.INVENTORY_ITEMS)
                for item in items:
                    name_elem = item.find_element(*self.ITEM_NAME)
                    if name_elem.text.strip().lower() == product_name.strip().lower():
                        price = item.find_element(*self.ITEM_PRICE).text
                        btn = item.find_element(By.TAG_NAME, "button")
                        driver.execute_script("arguments[0].click();", btn)
                        return {"name": name_elem.text, "price": price}
                return False
            except StaleElementReferenceException:
                return False

        return self.wait.until(_add_by_name, message=f"Product '{product_name}' not found or could not be added")

    def get_cart_badge_count(self) -> int:
        """Return the integer count displayed on the shopping cart badge."""
        badge_text = self.get_text(self.SHOPPING_CART_BADGE)
        return int(badge_text)

    def is_cart_badge_displayed(self) -> bool:
        """Check if shopping cart badge is currently visible."""
        return self.is_displayed(self.SHOPPING_CART_BADGE)

    def click_shopping_cart(self) -> None:
        """Click the shopping cart icon to navigate to the cart page."""
        self.js_click(self.SHOPPING_CART_LINK)
        self.wait_for_url_contains("/cart.html")
