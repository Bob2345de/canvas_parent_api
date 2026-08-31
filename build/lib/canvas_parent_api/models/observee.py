"""Observee Model Definition."""
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import ObserveeResponse
from typing import Optional

class Observee(DataModel):
    """Observee Model Definition."""
    def __init__(self, observee_resp: ObserveeResponse):
        self._id = observee_resp.id
        self._name = observee_resp.name
        self._created_at = observee_resp.created_at
        self._sortable_name = observee_resp.sortable_name
        self._short_name = observee_resp.short_name
        self._observation_link_root_account = observee_resp.observation_link_root_account

    @property
    def id(self) -> int:
        """Property Definition."""
        return self._id

    @property
    def name(self) -> str:
        """Property Definition."""
        return self._name

    @property
    def created_at(self) -> str:
        """Property Definition."""
        return self._created_at

    @property
    def sortable_name(self) -> str:
        """Property Definition."""
        return self._sortable_name

    @property
    def short_name(self) -> str:
        """Property Definition."""
        return self._short_name

    @property
    def observation_link_root_account(self) -> Optional[list[int]]:
        """Property Definition."""
        return self._observation_link_root_account
