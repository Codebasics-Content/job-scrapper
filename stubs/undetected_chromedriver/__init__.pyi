# Type stubs for undetected_chromedriver
# EMD Compliance: ≤80 lines

from selenium.webdriver.chrome.options import Options as SeleniumChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Any

class Chrome(WebDriver):
    """Undetected Chrome WebDriver - extends Selenium WebDriver"""
    
    def __init__(
        self,
        options: SeleniumChromeOptions | None = None,
        executable_path: str | None = None,
        port: int = 0,
        enable_cdp_events: bool = False,
        service_args: list[str] | None = None,
        desired_capabilities: dict[str, Any] | None = None,
        service_log_path: str | None = None,
        chrome_options: SeleniumChromeOptions | None = None,
        keep_alive: bool = True,
        log_level: int = 0,
        headless: bool = False,
        version_main: int | None = None,
        patcher_force_close: bool = False,
        suppress_welcome: bool = True,
        use_subprocess: bool = True,
        debug: bool = False,
        user_multi_procs: bool = False,
        **kwargs: Any
    ) -> None: ...
    
    def execute_script(self, script: str, *args: Any) -> Any: ...
    def quit(self) -> None: ...
    def close(self) -> None: ...
    def get(self, url: str) -> None: ...

class ChromeOptions(SeleniumChromeOptions):
    """Undetected ChromeOptions - extends Selenium ChromeOptions"""
    
    def __init__(self) -> None: ...
    def add_argument(self, argument: str) -> None: ...
    def add_experimental_option(self, name: str, value: Any) -> None: ...
    def set_capability(self, name: str, value: Any) -> None: ...

__all__ = ["Chrome", "ChromeOptions"]
