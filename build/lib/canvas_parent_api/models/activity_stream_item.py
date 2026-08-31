"""Activity Stream Item Model Definition."""
from typing import Optional
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import ActivityStreamItemResponse


class ActivityStreamItem(DataModel):
    """Activity Stream Item Model Definition."""
    def __init__(self, activity_stream_item_resp: ActivityStreamItemResponse):
        self._id = activity_stream_item_resp.id
        self._title = activity_stream_item_resp.title
        self._message = activity_stream_item_resp.message
        self._type = activity_stream_item_resp.type
        self._read_state = activity_stream_item_resp.read_state
        self._context_type = activity_stream_item_resp.context_type
        self._course_id = activity_stream_item_resp.course_id
        self._group_id = activity_stream_item_resp.group_id
        self._created_at = activity_stream_item_resp.created_at
        self._updated_at = activity_stream_item_resp.updated_at
        self._html_url = activity_stream_item_resp.html_url

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
    def type(self) -> Optional[str]:
        """Property Definition."""
        return self._type

    @property
    def read_state(self) -> Optional[bool]:
        """Property Definition."""
        return self._read_state

    @property
    def context_type(self) -> Optional[str]:
        """Property Definition."""
        return self._context_type

    @property
    def course_id(self) -> Optional[int]:
        """Property Definition."""
        return self._course_id

    @property
    def group_id(self) -> Optional[int]:
        """Property Definition."""
        return self._group_id

    @property
    def created_at(self) -> Optional[str]:
        """Property Definition."""
        return self._created_at

    @property
    def updated_at(self) -> Optional[str]:
        """Property Definition."""
        return self._updated_at

    @property
    def html_url(self) -> Optional[str]:
        """Property Definition."""
        return self._html_url
