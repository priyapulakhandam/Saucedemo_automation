"""Pytest fixtures and configuration for SauceDemo automation suite.

Includes:
- Chrome WebDriver fixture with headless/headed options
- Automatic screenshot on test failure saved to reports/screenshots/
- pytest-html extras integration embedding failure screenshots
- Pytest hooks for custom metadata and report formatting
"""

import os
import base64
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pytest_html import extras


def pytest_addoption(parser):
    """Add command line options for test execution."""
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Run browser in headed (visible) mode. Default is headless.",
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://www.saucedemo.com",
        help="Base URL for SauceDemo application under test.",
    )


@pytest.fixture(scope="session")
def base_url(request) -> str:
    """Fixture returning target application base URL."""
    return request.config.getoption("--base-url").rstrip("/")


@pytest.fixture(scope="function")
def driver(request):
    """WebDriver fixture initializing Chrome with recommended options.

    Tears down and closes browser after each test.
    """
    is_headed = request.config.getoption("--headed")

    chrome_options = Options()
    if not is_headed:
        chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")

    try:
        # Selenium 4 built-in Selenium Manager or webdriver-manager fallback
        driver_instance = webdriver.Chrome(options=chrome_options)
    except Exception:
        service = Service(ChromeDriverManager().install())
        driver_instance = webdriver.Chrome(service=service, options=chrome_options)

    # Attach driver to request node for screenshot hook access
    request.node.driver = driver_instance

    yield driver_instance

    driver_instance.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest hook to capture screenshots on test failure and embed in HTML report."""
    outcome = yield
    report = outcome.get_result()
    report_extras = getattr(report, "extras", [])

    if report.when == "call" and report.failed:
        driver_instance = getattr(item, "driver", None)
        if driver_instance is None:
            driver_instance = item.funcargs.get("driver", None)

        if driver_instance:
            screenshots_dir = os.path.join(os.path.dirname(__file__), "reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            safe_nodeid = item.name.replace("[", "_").replace("]", "_").replace(" ", "_")
            file_name = f"fail_{safe_nodeid}_{timestamp}.png"
            file_path = os.path.join(screenshots_dir, file_name)

            try:
                # 1. Save screenshot to disk
                driver_instance.save_screenshot(file_path)
                print(f"\n[FAILURE SCREENSHOT] Saved to: {file_path}")

                # 2. Attach base64 to pytest-html report
                screenshot_b64 = driver_instance.get_screenshot_as_base64()
                report_extras.append(extras.png(screenshot_b64))
                report_extras.append(extras.html(f"<div><b>Failure Screenshot:</b> {file_name}</div>"))
            except Exception as e:
                print(f"\n[FAILURE SCREENSHOT ERROR] Failed to capture: {e}")

    report.extras = report_extras


def pytest_html_report_title(report):
    """Set custom title for pytest-html report."""
    report.title = "SauceDemo UI Automation Test Report"
