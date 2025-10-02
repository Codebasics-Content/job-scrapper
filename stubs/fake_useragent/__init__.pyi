# Type stubs for fake_useragent
# EMD Compliance: ≤80 lines

class UserAgent:
    """Fake User Agent generator for anti-detection"""
    
    def __init__(
        self,
        browsers: list[str] | None = None,
        os: list[str] | None = None,
        min_version: float | None = None,
        fallback: str | None = None,
        use_cache_server: bool = True,
        verify_ssl: bool = True,
        safe_attrs: tuple[str, ...] | None = None
    ) -> None: ...
    
    @property
    def chrome(self) -> str:
        """Get Chrome user agent string"""
        ...
    
    @property
    def firefox(self) -> str:
        """Get Firefox user agent string"""
        ...
    
    @property
    def safari(self) -> str:
        """Get Safari user agent string"""
        ...
    
    @property
    def random(self) -> str:
        """Get random user agent string"""
        ...
    
    def __getitem__(self, name: str) -> str:
        """Get user agent by browser name"""
        ...
