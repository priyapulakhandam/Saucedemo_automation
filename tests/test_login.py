"""Test Suite: SauceDemo Login Functionality.

Covers:
- (a) Happy path login with standard_user asserting inventory URL and 'Products' title
- (b) Negative cases asserting exact error messages for locked_out_user and invalid password
- (f) Data-driven login testing loaded dynamically from data/login_data.json
"""

import json
import os
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def load_login_test_data():
    """Load login test datasets from JSON file."""
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "login_data.json")
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


LOGIN_TEST_DATA = load_login_test_data()


@pytest.mark.login
class TestLogin:
    """Test cases for user authentication on SauceDemo."""

    def test_login_happy_path(self, driver, base_url):
        """(a) Login, happy path: Log in as standard_user.

        Assert landing on the inventory page by verifying the URL contains
        '/inventory.html' and the page title is 'Products'.
        """
        login_page = LoginPage(driver, base_url).load()
        login_page.login(username="standard_user", password="secret_sauce")

        inventory_page = InventoryPage(driver, base_url).wait_until_loaded()

        # Assertions
        assert "/inventory.html" in inventory_page.get_current_url(), (
            f"Expected URL to contain '/inventory.html', but was '{inventory_page.get_current_url()}'"
        )
        assert inventory_page.get_title_text() == "Products", (
            f"Expected page title to be 'Products', but got '{inventory_page.get_title_text()}'"
        )

    def test_login_negative_locked_out_user(self, driver, base_url):
        """(b) Login negative: Locked out user.

        Log in as locked_out_user and assert the exact error message.
        """
        expected_error = "Epic sadface: Sorry, this user has been locked out."

        login_page = LoginPage(driver, base_url).load()
        login_page.login(username="locked_out_user", password="secret_sauce")

        assert login_page.is_error_displayed(), "Expected error message banner to be visible."
        actual_error = login_page.get_error_message()
        assert actual_error == expected_error, (
            f"Expected error message:\n'{expected_error}'\nbut got:\n'{actual_error}'"
        )

    def test_login_negative_wrong_password(self, driver, base_url):
        """(b) Login negative: Valid username with wrong password.

        Try a valid username (standard_user) with a wrong password and assert that error message too.
        """
        expected_error = "Epic sadface: Username and password do not match any user in this service"

        login_page = LoginPage(driver, base_url).load()
        login_page.login(username="standard_user", password="wrong_password_123")

        assert login_page.is_error_displayed(), "Expected error message banner to be visible."
        actual_error = login_page.get_error_message()
        assert actual_error == expected_error, (
            f"Expected error message:\n'{expected_error}'\nbut got:\n'{actual_error}'"
        )

    @pytest.mark.data_driven
    @pytest.mark.parametrize(
        "case",
        LOGIN_TEST_DATA,
        ids=[case["scenario"] for case in LOGIN_TEST_DATA],
    )
    def test_login_data_driven(self, driver, base_url, case):
        """(f) Data-driven login test executing scenarios loaded from JSON."""
        login_page = LoginPage(driver, base_url).load()
        login_page.login(username=case["username"], password=case["password"])

        if case["expected_result"] == "success":
            inventory_page = InventoryPage(driver, base_url).wait_until_loaded()
            assert case["expected_url_fragment"] in inventory_page.get_current_url()
            assert inventory_page.get_title_text() == case["expected_title"]
        else:
            assert login_page.is_error_displayed()
            actual_error = login_page.get_error_message()
            assert actual_error == case["expected_error"]
