"""Course Model Definition."""
from canvas_parent_api.base import DataModel
from canvas_parent_api.canvas_api_client import CourseResponse
from typing import Optional

class Course(DataModel):
    """Define Course Model."""
    def __init__(self, course_resp: CourseResponse):
        self._id = course_resp.id
        self._name = course_resp.name
        self._course_code = course_resp.course_code
        self._original_name = course_resp.original_name
        self._enrollment_term_id = course_resp.enrollment_term_id
        self._grading_periods = course_resp.grading_periods
        self._grading_standard_id = course_resp.grading_standard_id
        self._created_at = course_resp.created_at
        self._start_at = course_resp.start_at
        self._end_at = course_resp.end_at
        self._enrollments = course_resp.enrollments
        self._calendar = course_resp.calendar
        self._syllabus_body = course_resp.syllabus_body
        self._term = course_resp.term
        self._course_progress = course_resp.course_progress
        self._public_syllabus = course_resp.public_syllabus
        self._public_description = course_resp.public_description
        self._open_enrollment = course_resp.open_enrollment
        self._self_enrollment = course_resp.self_enrollment
        self._course_format = course_resp.course_format
        self._time_zone = course_resp.time_zone

    @property
    def id(self) -> int:
        """Property Definition."""
        return self._id

    @property
    def name(self) -> str:
        """Property Definition."""
        return self._name

    @property
    def course_code(self) -> str:
        """Property Definition."""
        return self._course_code

    @property
    def original_name(self) -> str:
        """Property Definition."""
        return self._original_name

    @property
    def enrollment_term_id(self) -> int:
        """Property Definition."""
        return self._enrollment_term_id

    @property
    def grading_periods(self) -> list[int]:
        """Property Definition."""
        return self._grading_periods

    @property
    def grading_standard_id(self) -> int:
        """Property Definition."""
        return self._grading_standard_id

    @property
    def created_at(self) -> str:
        """Property Definition."""
        return self._created_at

    @property
    def start_at(self) -> str:
        """Property Definition."""
        return self._start_at

    @property
    def end_at(self) -> str:
        """Property Definition."""
        return self._end_at

    @property
    def enrollments(self) -> list:
        """Property Definition."""
        return self._enrollments

    @property
    def calendar(self) -> dict:
        """Property Definition."""
        return self._calendar

    @property
    def syllabus_body(self) -> str:
        """Property Definition."""
        return self._syllabus_body

    @property
    def term(self) -> dict:
        """Property Definition."""
        return self._term

    @property
    def course_progress(self) -> int:
        """Property Definition."""
        return self._course_progress

    @property
    def public_syllabus(self) -> bool:
        """Property Definition."""
        return self._public_syllabus

    @property
    def public_description(self) -> str:
        """Property Definition."""
        return self._public_description

    @property
    def open_enrollment(self) -> bool:
        """Property Definition."""
        return self._open_enrollment

    @property
    def self_enrollment(self) -> bool:
        """Property Definition."""
        return self._self_enrollment

    @property
    def course_format(self) -> str:
        """Property Definition."""
        return self._course_format

    @property
    def time_zone(self) -> str:
        """Property Definition."""
        return self._time_zone
