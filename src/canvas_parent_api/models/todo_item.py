"""To-Do Item Model Definition."""
from typing import Optional
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import TodoItemResponse


class TodoItem(DataModel):
    """To-Do Item Model Definition.

    A Canvas to-do item wraps either an ``assignment`` or a ``quiz`` dict. The
    convenience properties (name, due_at, points_possible, course_id) pull the
    relevant value out of whichever payload is present so callers do not have to
    inspect the nested dictionaries themselves.
    """
    def __init__(self, todo_item_resp: TodoItemResponse):
        self._type = todo_item_resp.type
        self._assignment = todo_item_resp.assignment
        self._quiz = todo_item_resp.quiz
        self._ignore = todo_item_resp.ignore
        self._ignore_permanently = todo_item_resp.ignore_permanently
        self._html_url = todo_item_resp.html_url
        self._needs_grading_count = todo_item_resp.needs_grading_count
        self._context_type = todo_item_resp.context_type
        self._course_id = todo_item_resp.course_id
        self._group_id = todo_item_resp.group_id
        self._context_name = todo_item_resp.context_name
        self._visible_in_planner = todo_item_resp.visible_in_planner

    def _payload(self) -> dict:
        """Return the nested assignment or quiz dict (whichever is present)."""
        if isinstance(self._assignment, dict):
            return self._assignment
        if isinstance(self._quiz, dict):
            return self._quiz
        return {}

    @property
    def type(self) -> Optional[str]:
        """Property Definition."""
        return self._type

    @property
    def assignment(self) -> Optional[dict]:
        """Property Definition."""
        return self._assignment

    @property
    def quiz(self) -> Optional[dict]:
        """Property Definition."""
        return self._quiz

    @property
    def ignore(self) -> Optional[str]:
        """Property Definition."""
        return self._ignore

    @property
    def ignore_permanently(self) -> Optional[str]:
        """Property Definition."""
        return self._ignore_permanently

    @property
    def html_url(self) -> Optional[str]:
        """Property Definition."""
        return self._html_url

    @property
    def needs_grading_count(self) -> Optional[int]:
        """Property Definition."""
        return self._needs_grading_count

    @property
    def context_type(self) -> Optional[str]:
        """Property Definition."""
        return self._context_type

    @property
    def course_id(self) -> Optional[int]:
        """Course id of the to-do item (from the payload if not set directly)."""
        if self._course_id is not None:
            return self._course_id
        return self._payload().get("course_id")

    @property
    def group_id(self) -> Optional[int]:
        """Property Definition."""
        return self._group_id

    @property
    def context_name(self) -> Optional[str]:
        """Property Definition."""
        return self._context_name

    @property
    def visible_in_planner(self) -> Optional[bool]:
        """Property Definition."""
        return self._visible_in_planner

    @property
    def name(self) -> Optional[str]:
        """Human-readable title of the underlying assignment or quiz."""
        return self._payload().get("name") or self._payload().get("title")

    @property
    def due_at(self) -> Optional[str]:
        """Due date of the underlying assignment or quiz, if any."""
        return self._payload().get("due_at")

    @property
    def points_possible(self) -> Optional[float]:
        """Points possible for the underlying assignment or quiz, if any."""
        return self._payload().get("points_possible")
