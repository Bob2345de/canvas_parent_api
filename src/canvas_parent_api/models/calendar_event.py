"""Calendar Event Model Definition."""
from typing import Optional
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import CalendarEventResponse


class CalendarEvent(DataModel):
    """Calendar Event Model Definition."""
    def __init__(self, calendar_event_resp: CalendarEventResponse):
        self._id = calendar_event_resp.id
        self._title = calendar_event_resp.title
        self._description = calendar_event_resp.description
        self._start_at = calendar_event_resp.start_at
        self._end_at = calendar_event_resp.end_at
        self._all_day = calendar_event_resp.all_day
        self._location_name = calendar_event_resp.location_name
        self._location_address = calendar_event_resp.location_address
        self._context_code = calendar_event_resp.context_code
        self._context_name = calendar_event_resp.context_name
        self._type = calendar_event_resp.type
        self._html_url = calendar_event_resp.html_url
        self._hidden = calendar_event_resp.hidden
        self._assignment = calendar_event_resp.assignment

    @property
    def id(self) -> int:
        """Property Definition."""
        return self._id

    @property
    def title(self) -> Optional[str]:
        """Property Definition."""
        return self._title

    @property
    def description(self) -> Optional[str]:
        """Property Definition."""
        return self._description

    @property
    def start_at(self) -> Optional[str]:
        """Property Definition."""
        return self._start_at

    @property
    def end_at(self) -> Optional[str]:
        """Property Definition."""
        return self._end_at

    @property
    def all_day(self) -> Optional[bool]:
        """Property Definition."""
        return self._all_day

    @property
    def location_name(self) -> Optional[str]:
        """Property Definition."""
        return self._location_name

    @property
    def location_address(self) -> Optional[str]:
        """Property Definition."""
        return self._location_address

    @property
    def context_code(self) -> Optional[str]:
        """Property Definition."""
        return self._context_code

    @property
    def context_name(self) -> Optional[str]:
        """Property Definition."""
        return self._context_name

    @property
    def type(self) -> Optional[str]:
        """Property Definition."""
        return self._type

    @property
    def html_url(self) -> Optional[str]:
        """Property Definition."""
        return self._html_url

    @property
    def hidden(self) -> Optional[bool]:
        """Property Definition."""
        return self._hidden

    @property
    def assignment(self) -> Optional[dict]:
        """Property Definition."""
        return self._assignment
