"""Module Model Definition."""
from typing import Optional
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import ModuleResponse


class Module(DataModel):
    """Module Model Definition."""
    def __init__(self, module_resp: ModuleResponse):
        self._id = module_resp.id
        self._name = module_resp.name
        self._position = module_resp.position
        self._unlock_at = module_resp.unlock_at
        self._require_sequential_progress = module_resp.require_sequential_progress
        self._prerequisite_module_ids = module_resp.prerequisite_module_ids
        self._state = module_resp.state
        self._completed_at = module_resp.completed_at
        self._items_count = module_resp.items_count
        self._items = module_resp.items
        self._published = module_resp.published

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
    def unlock_at(self) -> Optional[str]:
        """Property Definition."""
        return self._unlock_at

    @property
    def require_sequential_progress(self) -> Optional[bool]:
        """Property Definition."""
        return self._require_sequential_progress

    @property
    def prerequisite_module_ids(self) -> Optional[list]:
        """Property Definition."""
        return self._prerequisite_module_ids

    @property
    def state(self) -> Optional[str]:
        """Property Definition."""
        return self._state

    @property
    def completed_at(self) -> Optional[str]:
        """Property Definition."""
        return self._completed_at

    @property
    def items_count(self) -> Optional[int]:
        """Property Definition."""
        return self._items_count

    @property
    def items(self) -> Optional[list]:
        """Property Definition."""
        return self._items

    @property
    def published(self) -> Optional[bool]:
        """Property Definition."""
        return self._published
