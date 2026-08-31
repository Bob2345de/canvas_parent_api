"""Assignment Model Definition."""
from typing import Optional
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import AssignmentResponse


class Assignment(DataModel):
    """Assignment Model Definition."""
    def __init__(self, assignment_resp: AssignmentResponse):
        self._id = assignment_resp.id
        self._name = assignment_resp.name
        self._description = assignment_resp.description
        self._created_at = assignment_resp.created_at
        self._updated_at = assignment_resp.updated_at
        self._due_at = assignment_resp.due_at
        self._lock_at = assignment_resp.lock_at
        self._unlock_at = assignment_resp.unlock_at
        self._course_id = assignment_resp.course_id
        self._assignment_group_id = assignment_resp.assignment_group_id
        self._points_possible = assignment_resp.points_possible
        self._has_submitted_submissions = assignment_resp.has_submitted_submissions
        self._quiz_id = assignment_resp.quiz_id
        self._discussion_topic = assignment_resp.discussion_topic
        self._submission = assignment_resp.submission
        self._rubric = assignment_resp.rubric
        self._can_submit = assignment_resp.can_submit
        self._important_dates = assignment_resp.important_dates

    @property
    def id(self) -> int:
        """Property Definition."""
        return self._id

    @property
    def name(self) -> Optional[str]:
        """Property Definition."""
        return self._name

    @property
    def description(self) -> Optional[str]:
        """Property Definition."""
        return self._description

    @property
    def created_at(self) -> Optional[str]:
        """Property Definition."""
        return self._created_at

    @property
    def updated_at(self) -> Optional[str]:
        """Property Definition."""
        return self._updated_at

    @property
    def due_at(self) -> Optional[str]:
        """Property Definition."""
        return self._due_at

    @property
    def lock_at(self) -> Optional[str]:
        """Property Definition."""
        return self._lock_at

    @property
    def unlock_at(self) -> Optional[str]:
        """Property Definition."""
        return self._unlock_at

    @property
    def course_id(self) -> Optional[int]:
        """Property Definition."""
        return self._course_id

    @property
    def assignment_group_id(self) -> Optional[int]:
        """Property Definition."""
        return self._assignment_group_id

    @property
    def points_possible(self) -> Optional[float]:
        """Property Definition."""
        return self._points_possible

    @property
    def has_submitted_submissions(self) -> Optional[bool]:
        """Property Definition."""
        return self._has_submitted_submissions

    @property
    def quiz_id(self) -> Optional[int]:
        """Property Definition."""
        return self._quiz_id

    @property
    def discussion_topic(self) -> Optional[dict]:
        """Property Definition."""
        return self._discussion_topic

    @property
    def submission(self) -> Optional[dict]:
        """Property Definition."""
        return self._submission

    @property
    def rubric(self) -> Optional[list]:
        """Property Definition."""
        return self._rubric

    @property
    def can_submit(self) -> Optional[bool]:
        """Property Definition."""
        return self._can_submit

    @property
    def important_dates(self) -> Optional[bool]:
        """Property Definition."""
        return self._important_dates
