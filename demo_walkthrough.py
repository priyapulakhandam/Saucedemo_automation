"""Interactive Walkthrough Script for Screen Recording / Video Submission.

Demonstrates all required flows visually on Chrome with clear console milestones:
  (a) Login, happy path
  (b) Login, negative cases (locked_out_user & invalid credentials)
  (c) Shopping cart (two items, badge count=2, names and prices match)
  (d) Checkout overview (tax & total arithmetic verification, finish & confirmation)
  (e) Checkout negative case (empty first name validation)

Run with:
    ./venv/bin/python demo_walkthrough.py
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_step_two_page import CheckoutStepTwoPage
from pages.checkout_complete_page import CheckoutCompletePage


def pause(seconds: float = 1.5):
    """Visual pause strictly for demonstration/recording observation."""
    time.sleep(seconds)


def run_walkthrough():
    print("=" * 70)
    print(">>> STARTING SAUCEDEMO AUTOMATION WALKTHROUGH DEMO <<<")
    print("=" * 70)

    options = Options()
    # Opens visible Chrome window for screen recording
    options.add_argument("--window-size=1280,800")
    driver = webdriver.Chrome(options=options)

    try:
        base_url = "https://www.saucedemo.com"

        # -------------------------------------------------------------
        # STEP 1: (b) Login Negative - Locked Out User
        # -------------------------------------------------------------
        print("\n[STEP 1/5] Demonstrating Negative Login: locked_out_user...")
        login_page = LoginPage(driver, base_url).load()
        pause(1)
        login_page.login("locked_out_user", "secret_sauce")
        pause(1)
        err1 = login_page.get_error_message()
        print(f" -> Displayed Error: {err1}")
        assert err1 == "Epic sadface: Sorry, this user has been locked out."

        # -------------------------------------------------------------
        # STEP 2: (b) Login Negative - Wrong Password
        # -------------------------------------------------------------
        print("\n[STEP 2/5] Demonstrating Negative Login: standard_user + wrong password...")
        login_page.load()
        pause(1)
        login_page.login("standard_user", "wrong_password_xyz")
        pause(1)
        err2 = login_page.get_error_message()
        print(f" -> Displayed Error: {err2}")
        assert err2 == "Epic sadface: Username and password do not match any user in this service"

        # -------------------------------------------------------------
        # STEP 3: (a) Login Happy Path
        # -------------------------------------------------------------
        print("\n[STEP 3/5] Demonstrating Happy Path Login: standard_user...")
        login_page.load()
        pause(1)
        login_page.login("standard_user", "secret_sauce")
        inventory_page = InventoryPage(driver, base_url).wait_until_loaded()
        print(f" -> Landed on URL: {inventory_page.get_current_url()}")
        print(f" -> Page Title: {inventory_page.get_title_text()}")
        assert "/inventory.html" in inventory_page.get_current_url()
        assert inventory_page.get_title_text() == "Products"
        pause(1)

        # -------------------------------------------------------------
        # STEP 4: (c) Cart - Add 2 Products and Verify Cart
        # -------------------------------------------------------------
        print("\n[STEP 4/5] Demonstrating Cart Flow: Adding 2 products...")
        p1 = inventory_page.add_product_to_cart_by_index(0)
        print(f" -> Added Item 1: {p1['name']} ({p1['price']})")
        pause(1)

        p2 = inventory_page.add_product_to_cart_by_index(1)
        print(f" -> Added Item 2: {p2['name']} ({p2['price']})")
        pause(1)

        badge_count = inventory_page.get_cart_badge_count()
        print(f" -> Shopping Cart Badge Count: {badge_count}")
        assert badge_count == 2

        print(" -> Navigating to Cart Page...")
        inventory_page.click_shopping_cart()
        cart_page = CartPage(driver, base_url).wait_until_loaded()
        cart_names = cart_page.get_cart_item_names()
        cart_prices = cart_page.get_cart_item_prices()
        print(f" -> Cart Items: {cart_names}")
        print(f" -> Cart Prices: {cart_prices}")
        assert cart_names == [p1["name"], p2["name"]]
        assert cart_prices == [p1["price"], p2["price"]]
        pause(1.5)

        # -------------------------------------------------------------
        # STEP 5: (e) Checkout Negative & (d) Checkout End-to-End
        # -------------------------------------------------------------
        print("\n[STEP 5/5] Demonstrating Checkout Workflows...")
        cart_page.click_checkout()
        step_one = CheckoutStepOnePage(driver, base_url).wait_until_loaded()

        # (e) Negative case: Empty First Name
        print(" -> Submitting empty First Name for negative validation...")
        step_one.enter_first_name("")
        step_one.enter_last_name("Doe")
        step_one.enter_postal_code("90210")
        step_one.click_continue()
        pause(1)
        checkout_err = step_one.get_error_message()
        print(f" -> Checkout Error Displayed: {checkout_err}")
        assert checkout_err == "Error: First Name is required"

        # (d) Happy path checkout
        print(" -> Entering valid customer details...")
        step_one.enter_first_name("Jane")
        pause(0.5)
        step_one.click_continue()

        step_two = CheckoutStepTwoPage(driver, base_url).wait_until_loaded()
        item_total = step_two.get_item_total_amount()
        tax = step_two.get_tax_amount()
        total = step_two.get_total_amount()
        print(f" -> Item Total: ${item_total:.2f}")
        print(f" -> Tax:        ${tax:.2f}")
        print(f" -> Total:      ${total:.2f}")
        print(f" -> Formula Check: {item_total} + {tax} = {round(item_total + tax, 2)} == {total}")
        assert total == round(item_total + tax, 2)
        pause(1.5)

        print(" -> Clicking Finish to finalize order...")
        step_two.click_finish()
        complete_page = CheckoutCompletePage(driver, base_url).wait_until_loaded()
        header = complete_page.get_confirmation_header()
        desc = complete_page.get_confirmation_description()
        print(f" -> Order Header: {header}")
        print(f" -> Order Description: {desc}")
        assert header == "Thank you for your order!"
        assert "Your order has been dispatched" in desc
        pause(2)

        print("\n" + "=" * 70)
        print(">>> ALL 5 ASSIGNMENT REQUIREMENTS COMPLETED SUCCESSFULLY! <<<")
        print("=" * 70)

    finally:
        driver.quit()


if __name__ == "__main__":
    run_walkthrough()
