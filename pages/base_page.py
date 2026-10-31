"""Base Page Object providing reusable explicit-wait browser interactions.

Strictly avoids time.sleep / Thread.sleep in favor of Selenium explicit waits
(WebDriverWait + ExpectedConditions).
"""

from typing import List, Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class BasePage:
    """Base class for all Page Objects in the framework."""

    DEFAULT_TIMEOUT: int = 10

    def __init__(self, driver: WebDriver, base_url: str = "https://www.saucedemo.com") -> None:
        self.driver: WebDriver = driver
        self.base_url: str = base_url.rstrip("/")
        self.wait: WebDriverWait = WebDriverWait(self.driver, self.DEFAULT_TIMEOUT)

    def open(self, path: str = "") -> None:
        """Navigate to a URL composed of base_url and optional path."""
        target_url = f"{self.base_url}/{path.lstrip('/')}" if path else self.base_url
        self.driver.get(target_url)

    def get_current_url(self) -> str:
        """Return the current browser URL."""
        return self.driver.current_url

    def get_title(self) -> str:
        """Return the current document title."""
        return self.driver.title

    def find(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Explicitly wait until element is visible and return it."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(
            EC.visibility_of_element_located(locator),
            message=f"Element located by {locator} not visible within {timeout or self.DEFAULT_TIMEOUT}s"
        )

    def find_presence(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """Explicitly wait until element is present in DOM and return it."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(
            EC.presence_of_element_located(locator),
            message=f"Element located by {locator} not present within {timeout or self.DEFAULT_TIMEOUT}s"
        )

    def find_all(self, locator: Tuple[str, str], timeout: int = None) -> List[WebElement]:
        """Explicitly wait until elements are present and return the list."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(
            EC.presence_of_all_elements_located(locator),
            message=f"Elements located by {locator} not present within {timeout or self.DEFAULT_TIMEOUT}s"
        )

    def click(self, locator: Tuple[str, str], timeout: int = None) -> None:
        """Explicitly wait until element is clickable and perform click.

        Falls back to JavaScript click if standard click is intercepted or blocked
        by overlay animations.
        """
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        element = wait.until(
            EC.element_to_be_clickable(locator),
            message=f"Element located by {locator} not clickable within {timeout or self.DEFAULT_TIMEOUT}s"
        )
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def js_click(self, locator: Tuple[str, str], timeout: int = None) -> None:
        """Explicitly wait until element is present and perform click via JavaScript.

        Guarantees dispatch of click events on React single-page app components
        even when nested badges or platform-specific cursor behaviors swallow native clicks.
        """
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        element = wait.until(
            EC.presence_of_element_located(locator),
            message=f"Element located by {locator} not present within {timeout or self.DEFAULT_TIMEOUT}s"
        )
        self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator: Tuple[str, str], text: str, clear_first: bool = True, timeout: int = None) -> None:
        """Explicitly wait until input is clickable, focus, optionally clear, and enter text.

        Includes React controlled component value synchronization to guarantee
        the input value is bound to React state across both headless and headed modes.
        """
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        element = wait.until(
            EC.element_to_be_clickable(locator),
            message=f"Element located by {locator} not clickable within {timeout or self.DEFAULT_TIMEOUT}s"
        )
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].focus();", element)

        if clear_first:
            element.clear()

        if text:
            element.send_keys(text)
            # Ensure React controlled input has successfully bound the value
            if element.get_attribute("value") != text:
                self.driver.execute_script(
                    """
                    var el = arguments[0];
                    var val = arguments[1];
                    var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                    setter.call(el, val);
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                    """,
                    element,
                    text,
                )
        elif clear_first and not text:
            # If explicit empty text requested, ensure React state is also cleared
            if element.get_attribute("value"):
                self.driver.execute_script(
                    """
                    var el = arguments[0];
                    var setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                    setter.call(el, '');
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                    """,
                    element,
                )

    def get_text(self, locator: Tuple[str, str], timeout: int = None) -> str:
        """Explicitly wait until element is visible and return its text."""
        return self.find(locator, timeout=timeout).text

    def is_displayed(self, locator: Tuple[str, str], timeout: int = 3) -> bool:
        """Check if an element is visible within timeout without throwing exception."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_url_contains(self, fragment: str, timeout: int = None) -> bool:
        """Explicitly wait until the current URL contains the expected fragment."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(
            EC.url_contains(fragment),
            message=f"URL did not contain '{fragment}' within {timeout or self.DEFAULT_TIMEOUT}s. Current URL: {self.driver.current_url}"
        )
