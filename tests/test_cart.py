"""Test Suite: SauceDemo Shopping Cart Functionality.

Covers:
- (c) Add any two products, assert the cart badge shows 2, and assert names
      and prices on the cart page match what you selected.
"""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@pytest.mark.cart
class TestCart:
    """Test cases for shopping cart operations."""

    def test_add_two_products_and_verify_cart(self, driver, base_url):
        """(c) Cart verification:

        1. Add any two products from inventory.
        2. Assert the cart badge shows 2.
        3. Navigate to Cart page.
        4. Assert the names and prices on the cart page match what was selected.
        """
        # Step 1: Login
        login_page = LoginPage(driver, base_url).load()
        login_page.login(username="standard_user", password="secret_sauce")

        inventory_page = InventoryPage(driver, base_url).wait_until_loaded()

        # Step 2: Add two distinct products to cart and store details
        first_product = inventory_page.add_product_to_cart_by_index(0)
        second_product = inventory_page.add_product_to_cart_by_index(1)

        expected_names = [first_product["name"], second_product["name"]]
        expected_prices = [first_product["price"], second_product["price"]]

        # Step 3: Assert the cart badge displays 2
        assert inventory_page.is_cart_badge_displayed(), "Shopping cart badge is not displayed."
        actual_badge_count = inventory_page.get_cart_badge_count()
        assert actual_badge_count == 2, (
            f"Expected cart badge count to be 2, but got {actual_badge_count}"
        )

        # Step 4: Navigate to Cart page
        inventory_page.click_shopping_cart()
        cart_page = CartPage(driver, base_url).wait_until_loaded()

        # Step 5: Assert names and prices on cart page match selected items
        actual_names = cart_page.get_cart_item_names()
        actual_prices = cart_page.get_cart_item_prices()

        assert len(actual_names) == 2, f"Expected 2 items in cart, found {len(actual_names)}"
        assert actual_names == expected_names, (
            f"Cart product names do not match.\nExpected: {expected_names}\nActual: {actual_names}"
        )
        assert actual_prices == expected_prices, (
            f"Cart product prices do not match.\nExpected: {expected_prices}\nActual: {actual_prices}"
        )
