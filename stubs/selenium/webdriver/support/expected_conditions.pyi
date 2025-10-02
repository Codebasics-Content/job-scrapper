"""Type stubs for selenium.webdriver.support.expected_conditions"""

from typing import Callable, Any
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

def presence_of_element_located(
    locator: tuple[str, str]
) -> Callable[[WebDriver], WebElement]: ...

def visibility_of_element_located(
    locator: tuple[str, str]
) -> Callable[[WebDriver], WebElement]: ...

def element_to_be_clickable(
    locator: tuple[str, str]
) -> Callable[[WebDriver], WebElement]: ...

def title_contains(
    title: str
) -> Callable[[WebDriver], bool]: ...

def url_contains(
    url: str
) -> Callable[[WebDriver], bool]: ...
