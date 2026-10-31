# SauceDemo End-to-End Automation Framework

A test automation solution built with **Python 3**, **Selenium WebDriver 4**, and **Pytest** for the [SauceDemo](https://www.saucedemo.com/) e-commerce web application.

---

## 📋 Assignment Requirements & Coverage Matrix

| Assignment Section | Points | Test Implementation | Key Assertions |
| :--- | :---: | :--- | :--- |
| **(a) Login Happy Path** | 2 pts | `tests/test_login.py::TestLogin::test_login_happy_path` | Verified landing on `/inventory.html` and page title is `"Products"` |
| **(b) Login Negative Cases** | 3 pts | `tests/test_login.py::TestLogin::test_login_negative_locked_out_user`<br>`tests/test_login.py::TestLogin::test_login_negative_wrong_password` | Exact message: `"Epic sadface: Sorry, this user has been locked out."`<br>Exact message: `"Epic sadface: Username and password do not match any user in this service"` |
| **(c) Cart Verification** | 3 pts | `tests/test_cart.py::TestCart::test_add_two_products_and_verify_cart` | Add 2 products, assert cart badge count is `2`, navigate to Cart, assert product names and prices match selected items |
| **(d) Checkout Happy Path & Math** | 3 pts | `tests/test_checkout.py::TestCheckout::test_checkout_end_to_end_and_calculation` | Complete checkout info, read Item Total, Tax, and Total on overview, assert `total == item_total + tax`, finish order, assert confirmation header (`"Thank you for your order!"`) and dispatch message |
| **(e) Checkout Negative Case** | 2 pts | `tests/test_checkout.py::TestCheckout::test_checkout_negative_empty_first_name`<br>`tests/test_checkout.py::TestCheckout::test_checkout_validation_matrix` | Submit empty first name, assert exact error message: `"Error: First Name is required"` (plus last name & postal code matrix) |
| **(f) Framework Quality** | 2 pts | `pages/`, `conftest.py`, `data/`, `pytest.ini` | • **Page Object Model (POM)** structure<br>• **Explicit waits exclusively** (`WebDriverWait` / `EC`, zero `time.sleep`)<br>• **Data-driven login test** loaded from `data/login_data.json`<br>• **Automatic screenshot on failure** in `reports/screenshots/` and embedded into HTML report<br>• **HTML test report** generated via `pytest-html` |

---

## 🏗️ Architecture & Directory Structure

```text
SauceDemo_Automation/
├── conftest.py                   # Pytest fixtures (Chrome options, driver teardown, failure screenshot hook)
├── pytest.ini                    # Pytest settings, markers, and HTML report flags
├── requirements.txt              # Project dependencies
├── demo_walkthrough.py           # Interactive visual walkthrough script for screen recording
├── data/
│   ├── login_data.json           # External JSON data source for data-driven login tests
│   └── checkout_data.json        # Test datasets for checkout validation matrix
├── pages/                        # Page Object Model (POM) Layer
│   ├── __init__.py
│   ├── base_page.py              # Base class encapsulating explicit waits and safe DOM interactions
│   ├── login_page.py             # Login form locators and actions
│   ├── inventory_page.py         # Products list, item cards, cart badge, navigation
│   ├── cart_page.py              # Shopping cart items, prices, and checkout button
│   ├── checkout_step_one_page.py # Customer information form and input validations
│   ├── checkout_step_two_page.py # Overview summary (item total, tax, total) and finish
│   └── checkout_complete_page.py # Order confirmation and dispatch messages
├── tests/                        # Test Suites
│   ├── __init__.py
│   ├── test_login.py             # (a) Happy path, (b) Negative cases, (f) Data-driven test
│   ├── test_cart.py              # (c) Add 2 products, badge count, names and prices verification
│   └── test_checkout.py          # (d) Checkout math & confirmation, (e) Missing first name validation
└── reports/                      # Test Execution Artifacts
    ├── report.html               # Self-contained HTML test report
    └── screenshots/              # Timestamped failure screenshots (.png)
```

---

## ⚙️ Key Technical Highlights

1. **Page Object Model (POM)**:
   - Clean separation of DOM locators, page action methods, and test assertions.
   - Robust locators using official `data-test` attributes (e.g. `[data-test="username"]`, `[data-test="shopping-cart-badge"]`, `[data-test="subtotal-label"]`).

2. **Strict Explicit Waits Only**:
   - Zero `time.sleep` or `Thread.sleep` throughout page objects and test suites.
   - Dynamic synchronization using `WebDriverWait` with expected conditions (`visibility_of_element_located`, `element_to_be_clickable`, `presence_of_all_elements_located`, `url_contains`).
   - Resilient DOM polling handles React single-page app re-renders without stale element exceptions.

3. **Data-Driven Testing**:
   - `tests/test_login.py::TestLogin::test_login_data_driven` reads test cases dynamically from `data/login_data.json` covering valid standard user, locked-out user, wrong password, empty username, and empty password.

4. **Automatic Screenshot on Failure**:
   - Configured in `conftest.py` through `pytest_runtest_makereport`.
   - When any test fails, a high-resolution screenshot is automatically saved to `reports/screenshots/fail_<test_name>_<timestamp>.png` and embedded directly as a base64 image inside `reports/report.html`.

5. **Self-Contained HTML Reporting**:
   - `pytest.ini` automatically outputs a styled, standalone HTML report (`reports/report.html`) containing summary statistics, execution time, pass/fail status, and embedded screenshots.

---

## 🚀 Setup & Execution Guide

### 1. Prerequisites
- Python 3.9+ installed
- Google Chrome browser installed

### 2. Environment Setup
```bash
# Clone or navigate to the project directory
cd SauceDemo_Automation

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run the Full Test Suite
```bash
# Run all tests in headless mode (default) and generate HTML report
pytest

# Run all tests with visible Chrome browser
pytest --headed

# Run with verbose console output
pytest -v
```

### 4. Run Specific Test Suites
```bash
# Run only login tests (including happy path, negative cases, data-driven)
pytest tests/test_login.py

# Run only shopping cart tests
pytest tests/test_cart.py

# Run only checkout tests
pytest tests/test_checkout.py

# Run by pytest marker
pytest -m login
pytest -m cart
pytest -m checkout
pytest -m data_driven
```

### 5. View Test Reports
```bash
# Open the generated HTML test report in your browser (macOS)
open reports/report.html

# On Linux:
# xdg-open reports/report.html
```

---

## 📹 Walkthrough Video Recording Guide

To record the required walkthrough video for your submission, an interactive runner script `demo_walkthrough.py` is included:

```bash
# Launch interactive visual walkthrough with paced step-by-step progress
python demo_walkthrough.py
```
