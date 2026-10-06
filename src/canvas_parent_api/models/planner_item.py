"""Planner Item Model Definition."""
from typing import Optional
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import PlannerItemResponse


class PlannerItem(DataModel):
    """Planner Item Model Definition.

    Wraps one entry from GET /api/v1/users/:user_id/planner/items. Unlike the
    calendar endpoint these items carry the title directly and the date under
    ``date``; convenience properties also expose submission/override state so
    callers can tell whether the item was already submitted or marked complete.
    """
    def __init__(self, planner_item_resp: PlannerItemResponse):
        self._context_code = planner_item_resp.context_code
        self._context_name = planner_item_resp.context_name
        self._course_id = planner_item_resp.course_id
        self._group_id = planner_item_resp.group_id
        self._type = planner_item_resp.type
        self._date = planner_item_resp.date
        self._title = planner_item_resp.title
        self._points_possible = planner_item_resp.points_possible
        self._html_url = planner_item_resp.html_url
        self._planner_override = planner_item_resp.planner_override or {}
        self._submissions = planner_item_resp.submissions or {}
        self._new_activity = planner_item_resp.new_activity

    @property
    def context_code(self) -> Optional[str]:
        """Property Definition."""
        return self._context_code

    @property
    def context_name(self) -> Optional[str]:
        """Property Definition."""
        return self._context_name

    @property
    def course_id(self) -> Optional[int]:
        """Property Definition."""
        return self._course_id

    @property
    def group_id(self) -> Optional[int]:
        """Property Definition."""
        return self._group_id

    @property
    def type(self) -> Optional[str]:
        """Item kind, e.g. 'assignment', 'Quiz', 'Discussion', 'Announcement', 'Calendar Event'."""
        return self._type

    @property
    def date(self) -> Optional[str]:
        """ISO-8601 date/due date of the item."""
        return self._date

    @property
    def due_at(self) -> Optional[str]:
        """Alias of ``date`` so callers can sort/treat it like a due date."""
        return self._date

    @property
    def name(self) -> Optional[str]:
        """Human-readable title of the item."""
        return self._title

    @property
    def title(self) -> Optional[str]:
        """Alias of ``name``."""
        return self._title

    @property
    def points_possible(self) -> Optional[float]:
        """Property Definition."""
        return self._points_possible

    @property
    def html_url(self) -> Optional[str]:
        """Property Definition."""
        return self._html_url

    @property
    def planner_override(self) -> dict:
        """Planner override dict (may hold 'marked_complete' / 'dismissed')."""
        return self._planner_override

    @property
    def submissions(self) -> dict:
        """Submission dict for this item, if any."""
        return self._submissions

    @property
    def new_activity(self) -> Optional[bool]:
        """True if the item has new/unread activity."""
        return self._new_activity

    @property
    def marked_complete(self) -> bool:
        """True if the planner override marks the item complete."""
        return bool(self._planner_override.get("marked_complete"))

    @property
    def submitted(self) -> bool:
        """True if the item's submission is submitted (or has a grade)."""
        state = self._submissions.get("workflow_state") or ""
        return state in ("submitted", "graded") or self._submissions.get("submitted_at") is not None