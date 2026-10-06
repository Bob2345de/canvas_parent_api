"""Planner Item Model Definition."""
from typing import Optional
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import PlannerItemResponse


class PlannerItem(DataModel):
    """Planner Item Model Definition.

    Wraps one entry from GET /api/v1/users/:user_id/planner/items. Canvas nests
    the human-readable name and points inside ``plannable``, puts the date under
    ``plannable_date`` and the kind under ``plannable_type``. The convenience
    properties flatten those and expose submission/override state.
    """
    def __init__(self, planner_item_resp: PlannerItemResponse):
        self._context_type = planner_item_resp.context_type
        self._context_name = planner_item_resp.context_name
        self._course_id = planner_item_resp.course_id
        self._group_id = planner_item_resp.group_id
        self._plannable_type = planner_item_resp.plannable_type
        self._plannable_date = planner_item_resp.plannable_date
        self._plannable = planner_item_resp.plannable or {}
        self._html_url = planner_item_resp.html_url
        self._planner_override = planner_item_resp.planner_override or {}
        self._submissions = planner_item_resp.submissions or {}
        self._new_activity = planner_item_resp.new_activity

    @property
    def context_type(self) -> Optional[str]:
        """Context kind, e.g. 'Course' or 'Group'."""
        return self._context_type

    @property
    def context_code(self) -> Optional[str]:
        """e.g. 'course_15906' — derived (lowercased) from context_type plus course/group id."""
        if self._course_id is not None:
            return f"{(self._context_type or 'course').lower()}_{self._course_id}"
        if self._group_id is not None:
            return f"{(self._context_type or 'group').lower()}_{self._group_id}"
        return None

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
        return self._plannable_type

    @property
    def plannable_type(self) -> Optional[str]:
        """Alias of ``type``."""
        return self._plannable_type

    @property
    def due_at(self) -> Optional[str]:
        """Planner date of the item; falls back to the plannable's own due_at."""
        return self._plannable_date or (self._plannable or {}).get("due_at")

    @property
    def date(self) -> Optional[str]:
        """Alias of ``due_at``."""
        return self.due_at

    @property
    def name(self) -> Optional[str]:
        """Human-readable title, read from the nested plannable payload."""
        return (self._plannable or {}).get("title") or (self._plannable or {}).get("name")

    @property
    def title(self) -> Optional[str]:
        """Alias of ``name``."""
        return self.name

    @property
    def points_possible(self) -> Optional[float]:
        """Points possible for the item (from the nested plannable payload)."""
        return (self._plannable or {}).get("points_possible")

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
        """True if the item's submission is submitted or graded.

        Handles both the boolean ``submissions.submitted`` flag used by the
        planner endpoint and the ``workflow_state`` / ``submitted_at`` fields.
        """
        if self._submissions.get("submitted") is True:
            return True
        state = self._submissions.get("workflow_state") or ""
        if state in ("submitted", "graded"):
            return True
        return self._submissions.get("submitted_at") is not None