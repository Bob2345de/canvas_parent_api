"""Teacher Model Definition."""
from typing import Optional
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import TeacherResponse


class Teacher(DataModel):
    """Teacher Model Definition."""
    def __init__(self, teacher_resp: TeacherResponse):
        self._id = teacher_resp.id
        self._name = teacher_resp.name
        self._sortable_name = teacher_resp.sortable_name
        self._short_name = teacher_resp.short_name
        self._email = teacher_resp.email
        self._avatar_url = teacher_resp.avatar_url
        self._bio = teacher_resp.bio
        self._pronouns = teacher_resp.pronouns

    @property
    def id(self) -> int:
        """Property Definition."""
        return self._id

    @property
    def name(self) -> Optional[str]:
        """Property Definition."""
        return self._name

    @property
    def sortable_name(self) -> Optional[str]:
        """Property Definition."""
        return self._sortable_name

    @property
    def short_name(self) -> Optional[str]:
        """Property Definition."""
        return self._short_name

    @property
    def email(self) -> Optional[str]:
        """Property Definition."""
        return self._email

    @property
    def avatar_url(self) -> Optional[str]:
        """Property Definition."""
        return self._avatar_url

    @property
    def bio(self) -> Optional[str]:
        """Property Definition."""
        return self._bio

    @property
    def pronouns(self) -> Optional[str]:
        """Property Definition."""
        return self._pronouns
