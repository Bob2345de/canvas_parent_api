"""Assignment Group Model Definition."""
from typing import Optional
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import AssignmentGroupResponse


class AssignmentGroup(DataModel):
    """Assignment Group Model Definition."""
    def __init__(self, assignment_group_resp: AssignmentGroupResponse):
        self._id = assignment_group_resp.id
        self._name = assignment_group_resp.name
        self._position = assignment_group_resp.position
        self._group_weight = assignment_group_resp.group_weight
        self._rules = assignment_group_resp.rules
        self._assignments = assignment_group_resp.assignments

    @property
    def id(self) -> int:
        """Property Definition."""
        return self._id

    @property
    def name(self) -> Optional[str]:
        """Property Definition."""
        return self._name

    @property
    def position(self) -> Optional[int]:
        """Property Definition."""
        return self._position

    @property
    def group_weight(self) -> Optional[float]:
        """Property Definition."""
        return self._group_weight

    @property
    def rules(self) -> Optional[dict]:
        """Property Definition."""
        return self._rules

    @property
    def assignments(self) -> Optional[list]:
        """Property Definition."""
        return self._assignments
