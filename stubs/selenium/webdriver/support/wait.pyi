"""Type stubs for selenium.webdriver.support.wait"""

from typing import Any, Callable, TypeVar
from selenium.webdriver.remote.webdriver import WebDriver

_T = TypeVar("_T")

class WebDriverWait:
    def __init__(
        self,
        driver: WebDriver,
        timeout: float,
        poll_frequency: float = 0.5,
        ignored_exceptions: Any = None
    ) -> None: ...
    
    def until(
        self,
        method: Callable[[WebDriver], _T],
        message: str = ""
    ) -> _T: ...
    
    def until_not(
        self,
        method: Callable[[WebDriver], _T],
        message: str = ""
    ) -> _T: ...
