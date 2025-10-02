# Type stubs for BeautifulSoup4
# EMD Compliance: ≤80 lines

from typing import Any, Iterator, SupportsIndex, overload

class Tag:
    """BeautifulSoup Tag element with CSS selector support"""
    name: str
    attrs: dict[str, str | list[str]]
    string: str | None
    text: str
    
    def select_one(
        self,
        selector: str,
        namespaces: dict[str, str] | None = None,
        **kwargs: Any
    ) -> Tag | None: ...
    
    def select(
        self,
        selector: str,
        namespaces: dict[str, str] | None = None,
        limit: int | None = None,
        **kwargs: Any
    ) -> ResultSet: ...
    
    def find(
        self,
        name: str | None = None,
        attrs: dict[str, Any] | None = None,
        **kwargs: Any
    ) -> Tag | None: ...
    
    def find_all(
        self,
        name: str | None = None,
        attrs: dict[str, Any] | None = None,
        limit: int | None = None,
        **kwargs: Any
    ) -> ResultSet: ...
    
    def get(self, key: str, default: Any = None) -> Any: ...
    def get_text(self, separator: str = "", strip: bool = False) -> str: ...

class ResultSet(list[Tag]):
    """Collection of Tag elements from search results"""
    @overload
    def __getitem__(self, key: SupportsIndex) -> Tag: ...
    @overload
    def __getitem__(self, key: slice) -> list[Tag]: ...

class BeautifulSoup(Tag):
    """Main BeautifulSoup parser class"""
    def __init__(
        self,
        markup: str | bytes = "",
        features: str | None = None,
        **kwargs: Any
    ) -> None: ...

__all__ = ["BeautifulSoup", "Tag", "ResultSet"]
