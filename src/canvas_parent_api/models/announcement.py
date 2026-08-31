"""Announcement Model Definition."""
from typing import Optional
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import AnnouncementResponse


class Announcement(DataModel):
    """Announcement Model Definition."""
    def __init__(self, announcement_resp: AnnouncementResponse):
        self._id = announcement_resp.id
        self._title = announcement_resp.title
        self._message = announcement_resp.message
        self._posted_at = announcement_resp.posted_at
        self._delayed_post_at = announcement_resp.delayed_post_at
        self._context_code = announcement_resp.context_code
        self._read_state = announcement_resp.read_state
        self._html_url = announcement_resp.html_url
        self._url = announcement_resp.url
        self._author = announcement_resp.author

    @property
    def id(self) -> int:
        """Property Definition."""
        return self._id

    @property
    def title(self) -> Optional[str]:
        """Property Definition."""
        return self._title

    @property
    def message(self) -> Optional[str]:
        """Property Definition."""
        return self._message

    @property
    def posted_at(self) -> Optional[str]:
        """Property Definition."""
        return self._posted_at

    @property
    def delayed_post_at(self) -> Optional[str]:
        """Property Definition."""
        return self._delayed_post_at

    @property
    def context_code(self) -> Optional[str]:
        """Property Definition."""
        return self._context_code

    @property
    def read_state(self) -> Optional[str]:
        """Property Definition."""
        return self._read_state

    @property
    def html_url(self) -> Optional[str]:
        """Property Definition."""
        return self._html_url

    @property
    def url(self) -> Optional[str]:
        """Property Definition."""
        return self._url

    @property
    def author(self) -> Optional[dict]:
        """Property Definition."""
        return self._author
