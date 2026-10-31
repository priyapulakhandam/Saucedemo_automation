"""Test Suite: SauceDemo Checkout Workflow.

Covers:
- (d) Complete checkout form, read item total, tax, and total on overview page,
      assert that total = item total + tax, finish order, and assert confirmation message.
- (e) Submit checkout form with empty first name and assert validation error message.
- Additional edge case tests for complete failure-path coverage.
"""

import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_step_two_page import CheckoutStepTwoPage
from pages.checkout_complete_page import CheckoutCompletePage


@pytest.mark.checkout
class TestCheckout:
    """Test cases for SauceDemo checkout and order fulfillment flows."""

    def test_checkout_end_to_end_and_calculation(self, driver, base_url):
        """(d) Checkout happy path:

        1. Complete login and add products to cart.
        2. Navigate through cart to checkout step one.
        3. Fill customer information and submit.
        4. Read item total, tax, and total from overview page.
        5. Assert that total == item total + tax.
        6. Finish the order.
        7. Assert order confirmation header and dispatch message.
        """
        # Step 1: Login & add products
        login_page = LoginPage(driver, base_url).load()
        login_page.login(username="standard_user", password="secret_sauce")

        inventory_page = InventoryPage(driver, base_url).wait_until_loaded()
        inventory_page.add_product_to_cart_by_index(0)
        inventory_page.add_product_to_cart_by_index(1)

        # Step 2: Navigate to Cart -> Checkout Step One
        inventory_page.click_shopping_cart()
        cart_page = CartPage(driver, base_url).wait_until_loaded()
        cart_page.click_checkout()

        # Step 3: Complete checkout customer information form
        step_one = CheckoutStepOnePage(driver, base_url).wait_until_loaded()
        step_one.submit_information(first_name="Jane", last_name="Doe", postal_code="90210")

        # Step 4: Validate overview amounts and total formula
        step_two = CheckoutStepTwoPage(driver, base_url).wait_until_loaded()

        item_total = step_two.get_item_total_amount()
        tax = step_two.get_tax_amount()
        total = step_two.get_total_amount()

        calculated_expected_total = round(item_total + tax, 2)
        assert total == calculated_expected_total, (
            f"Tax calculation mismatch!\n"
            f"Item Total: {item_total} + Tax: {tax} = {calculated_expected_total}, "
            f"but displayed Total is {total}"
        )

        # Step 5: Finish order and assert confirmation
        step_two.click_finish()
        complete_page = CheckoutCompletePage(driver, base_url).wait_until_loaded()

        expected_header = "Thank you for your order!"
        expected_msg_fragment = "Your order has been dispatched"

        actual_header = complete_page.get_confirmation_header()
        actual_description = complete_page.get_confirmation_description()

        assert actual_header == expected_header, (
            f"Expected confirmation header '{expected_header}', but got '{actual_header}'"
        )
        assert expected_msg_fragment in actual_description, (
            f"Expected description to contain '{expected_msg_fragment}', but got '{actual_description}'"
        )

    def test_checkout_negative_empty_first_name(self, driver, base_url):
        """(e) Checkout negative case:

        Submit the checkout form with an empty first name and assert
        the exact validation error message.
        """
        expected_error = "Error: First Name is required"

        # Login and add product to reach checkout
        login_page = LoginPage(driver, base_url).load()
        login_page.login(username="standard_user", password="secret_sauce")

        inventory_page = InventoryPage(driver, base_url).wait_until_loaded()
        inventory_page.add_product_to_cart_by_index(0)
        inventory_page.click_shopping_cart()

        cart_page = CartPage(driver, base_url).wait_until_loaded()
        cart_page.click_checkout()

        # On Step One, leave first name empty and submit
        step_one = CheckoutStepOnePage(driver, base_url).wait_until_loaded()
        step_one.enter_first_name("")
        step_one.enter_last_name("Doe")
        step_one.enter_postal_code("90210")
        step_one.click_continue()

        # Assert validation error message
        assert step_one.is_error_displayed(), "Expected validation error banner to appear."
        actual_error = step_one.get_error_message()
        assert actual_error == expected_error, (
            f"Expected error message:\n'{expected_error}'\nbut got:\n'{actual_error}'"
        )

    @pytest.mark.parametrize(
        "first_name,last_name,postal_code,expected_error",
        [
            ("", "Doe", "12345", "Error: First Name is required"),
            ("Jane", "", "12345", "Error: Last Name is required"),
            ("Jane", "Doe", "", "Error: Postal Code is required"),
        ],
        ids=["missing_first_name", "missing_last_name", "missing_postal_code"],
    )
    def test_checkout_validation_matrix(self, driver, base_url, first_name, last_name, postal_code, expected_error):
        """Failure-path coverage: Assert field-level validations for all required inputs."""
        login_page = LoginPage(driver, base_url).load()
        login_page.login(username="standard_user", password="secret_sauce")

        inventory_page = InventoryPage(driver, base_url).wait_until_loaded()
        inventory_page.add_product_to_cart_by_index(0)
        inventory_page.click_shopping_cart()

        cart_page = CartPage(driver, base_url).wait_until_loaded()
        cart_page.click_checkout()

        step_one = CheckoutStepOnePage(driver, base_url).wait_until_loaded()
        step_one.fill_information(first_name, last_name, postal_code)
        step_one.click_continue()

        assert step_one.is_error_displayed()
        assert step_one.get_error_message() == expected_error
