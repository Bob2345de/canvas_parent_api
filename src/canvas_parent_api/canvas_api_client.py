"""Canvas API Client."""
import json
import logging

from urllib.parse import urljoin

import aiohttp
from multidict import MultiDict

from canvas_parent_api.errors.canvas_error import CanvasError

from .models.base import (
    ObserveeResponse,
    CourseResponse,
    AssignmentResponse,
    SubmissionResponse,
    AnnouncementResponse,
    CalendarEventResponse,
    AssignmentGroupResponse,
    TeacherResponse,
    ModuleResponse,
    ActivityStreamItemResponse,
)

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


def _enable_debug_logging():
    _LOGGER.setLevel(logging.DEBUG)


class CanvasApiClient():
    """Canvas Parent API Client."""
    def __init__(
        self,
        base_url,
        api_key,
        path: str = None,
        debug=False,
    ):
        if debug:
            _enable_debug_logging()

        if path:
            self._base_url = f"{base_url}/api/v1/users/{path}"
        else:
            self._base_url = f"{base_url}/api/v1/"

        _LOGGER.debug(f"generated base url: {self._base_url}")

        self._api_key = api_key
        self._headers = {"accept": "application/json", "Authorization": f"Bearer {self._api_key}"}

    async def _get_request(self, end_url: str):
        """Perform GET request to API endpoint."""
        request_url = urljoin(self._base_url, end_url)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{request_url}", headers=self._headers) as resp:
                response = resp
                responsetext = await resp.text()
                if response.status >= 400:
                    raise CanvasError(response.status, responsetext)
                return response

    async def _get_paginated(self, end_url: str) -> list:
        """Perform GET request, following all pagination links."""
        parsed_json = []
        next_url = end_url
        while next_url:
            response = await self._get_request(next_url)
            parsed_json.extend(await response.json())
            next = MultiDict(response.links.get('next', ''))
            next_url = str(next.get('url')).replace(self._base_url, '') if next else None
        return parsed_json

    async def get_observees(self) -> list[ObserveeResponse]:
        """Get Canvas Observees (students)."""
        parsed_json = await self._get_paginated("users/self/observees?per_page=50")
        return [ObserveeResponse(**resp) for resp in parsed_json]

    async def get_courses(self, student_id: int, enrollment_state: str = "active") -> list[CourseResponse]:
        """Get Canvas Courses.

        By default only courses the student is actively enrolled in are returned.
        Canvas otherwise includes concluded enrollments, which brings back courses
        from previous school years.

        :param student_id: Canvas user id of the student.
        :param enrollment_state: 'active', 'invited_or_pending' or 'completed'.
            Pass None/empty to let Canvas apply its own default (active + completed).
        """
        end_url = (
            f"users/{student_id}/courses?include[]=term"
            "&include[]=current_grading_period_scores&include[]=total_scores&per_page=50"
        )
        if enrollment_state:
            end_url += f"&enrollment_state={enrollment_state}"
        parsed_json = await self._get_paginated(end_url)
        return [CourseResponse(**resp) for resp in parsed_json]

    async def get_assignments(self, student_id: int, course_id: int) -> list[AssignmentResponse]:
        """Get Canvas Assignments for a student in a course."""
        parsed_json = await self._get_paginated(
            f"users/{student_id}/courses/{course_id}/assignments?include[]=submission&per_page=50"
        )
        return [AssignmentResponse(**resp) for resp in parsed_json]

    async def get_submissions(self, student_id: int, course_id: int) -> list[SubmissionResponse]:
        """Get Canvas Submissions for a student in a course."""
        parsed_json = await self._get_paginated(
            f"courses/{course_id}/students/submissions?student_ids[]={student_id}&per_page=50"
        )
        return [SubmissionResponse(**resp) for resp in parsed_json]

    async def get_announcements(self, course_id: int, start_date: str = None, end_date: str = None) -> list[AnnouncementResponse]:
        """Get Canvas Announcements for a course."""
        end_url = f"announcements?context_codes[]=course_{course_id}&per_page=50"
        if start_date:
            end_url += f"&start_date={start_date}"
        if end_date:
            end_url += f"&end_date={end_date}"
        parsed_json = await self._get_paginated(end_url)
        return [AnnouncementResponse(**resp) for resp in parsed_json]

    async def get_calendar_events(self, student_id: int, start_date: str = None, end_date: str = None, event_type: str = "event") -> list[CalendarEventResponse]:
        """Get Canvas Calendar Events for a student."""
        end_url = f"users/{student_id}/calendar_events?type={event_type}&per_page=50"
        if start_date:
            end_url += f"&start_date={start_date}"
        if end_date:
            end_url += f"&end_date={end_date}"
        parsed_json = await self._get_paginated(end_url)
        return [CalendarEventResponse(**resp) for resp in parsed_json]

    async def get_assignment(self, course_id: int, assignment_id: int) -> AssignmentResponse:
        """Get a single Canvas Assignment with submission details."""
        response = await self._get_request(
            f"courses/{course_id}/assignments/{assignment_id}?include[]=submission"
        )
        parsed_json = await response.json()
        return AssignmentResponse(**parsed_json)

    async def get_assignment_groups(self, course_id: int) -> list[AssignmentGroupResponse]:
        """Get Canvas Assignment Groups (grade categories) for a course."""
        parsed_json = await self._get_paginated(
            f"courses/{course_id}/assignment_groups?include[]=assignments&include[]=submission&per_page=50"
        )
        return [AssignmentGroupResponse(**resp) for resp in parsed_json]

    async def get_course(self, course_id: int) -> CourseResponse:
        """Get a single Canvas Course including syllabus body."""
        response = await self._get_request(
            f"courses/{course_id}?include[]=syllabus_body&include[]=term&include[]=public_description"
        )
        parsed_json = await response.json()
        return CourseResponse(**parsed_json)

    async def get_teachers(self, course_id: int) -> list[TeacherResponse]:
        """Get Canvas Teachers for a course."""
        parsed_json = await self._get_paginated(
            f"courses/{course_id}/users?enrollment_type[]=teacher&include[]=email&include[]=avatar_url&include[]=bio&per_page=50"
        )
        return [TeacherResponse(**resp) for resp in parsed_json]

    async def get_modules(self, course_id: int, student_id: int = None) -> list[ModuleResponse]:
        """Get Canvas Modules with items and completion state for a course."""
        end_url = f"courses/{course_id}/modules?include[]=items&per_page=50"
        if student_id:
            end_url += f"&student_id={student_id}"
        parsed_json = await self._get_paginated(end_url)
        return [ModuleResponse(**resp) for resp in parsed_json]

    async def get_activity_stream(self, only_active_courses: bool = True) -> list[ActivityStreamItemResponse]:
        """Get the Canvas Activity Stream for the current user."""
        end_url = "users/self/activity_stream?per_page=50"
        if only_active_courses:
            end_url += "&only_active_courses=true"
        parsed_json = await self._get_paginated(end_url)
        return [ActivityStreamItemResponse(**resp) for resp in parsed_json]
