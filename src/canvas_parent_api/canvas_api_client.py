"""Canvas API Client."""
import json
import logging
import os
import tempfile
import threading
import time
import traceback

from datetime import datetime
from typing import Optional
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
    TodoItemResponse,
)

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


def _enable_debug_logging():
    _LOGGER.setLevel(logging.DEBUG)


# ---------------------------------------------------------------------------
# Per-call request/response logging to a text file
# ---------------------------------------------------------------------------
# Open WebUI stores its data (incl. the volume-mount "/app/backend/data" ->
# host "./data") here, so this path is accessible both inside the container and
# from the host. Override with the CANVAS_API_LOG_FILE environment variable.
_DEFAULT_API_LOG_PATH = "/app/backend/data/canvas_api.log"
_API_LOG_MAX_BODY = int(os.environ.get("CANVAS_API_LOG_MAX_BODY", "20000"))


def _resolve_api_log_path() -> Optional[str]:
    """Pick the first writable path for the API call log.

    Order: $CANVAS_API_LOG_FILE, the Open WebUI data dir (default, volume-mounted
    in the Docker container), the user home dir (local runs), the system temp
    dir. Returns None when no path is writable (call logging is then disabled).
    """
    candidates = []
    env_path = (os.environ.get("CANVAS_API_LOG_FILE") or "").strip()
    if env_path:
        candidates.append(env_path)
    candidates += [
        _DEFAULT_API_LOG_PATH,
        os.path.join(os.path.expanduser("~"), ".canvas_api.log"),
        os.path.join(tempfile.gettempdir(), "canvas_api.log"),
    ]
    for path in candidates:
        try:
            parent = os.path.dirname(path)
            if parent and not os.path.isdir(parent):
                continue
            with open(path, "a", encoding="utf-8"):
                pass
            return path
        except OSError:
            continue
    return None


API_LOG_PATH = _resolve_api_log_path()
_api_log_lock = threading.Lock()


def _api_log_line(line: str) -> None:
    """Append one line to the API log file (best effort, thread safe, flushed)."""
    if not API_LOG_PATH:
        return
    try:
        with _api_log_lock:
            with open(API_LOG_PATH, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")
    except OSError:
        pass


def _mask_api_key(api_key: str) -> str:
    """Show a small prefix/suffix of the key so log lines identify the token without leaking it."""
    if not api_key:
        return "<empty>"
    if len(api_key) <= 12:
        return f"{api_key[:4]}…{api_key[-2:]}"
    return f"{api_key[:6]}…{api_key[-4:]}"


def _now() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def _log_request(method: str, url: str, caller: str, masked_key: str) -> None:
    caller_txt = f" | caller={caller}" if caller else ""
    _api_log_line(f"{_now()} | REQUEST  | {method} {url} | token={masked_key}{caller_txt}")


def _log_response(status: int, body: str, elapsed_ms: float, url: str) -> None:
    if len(body) > _API_LOG_MAX_BODY:
        body_txt = f"{body[:_API_LOG_MAX_BODY]}\n… (truncated, {len(body)} chars total)"
    else:
        body_txt = body
    _api_log_line(f"{_now()} | RESPONSE | {status} in {elapsed_ms:.0f} ms | {url}\n{body_txt}")


def _log_failure(url: str, elapsed_ms: float, exc: BaseException) -> None:
    detail = "".join(traceback.format_exception_only(type(exc), exc)).strip()
    _api_log_line(f"{_now()} | ERROR    | FAILED after {elapsed_ms:.0f} ms | {url} | {detail}")


class CanvasApiClient():
    """Canvas Parent API Client."""
    def __init__(
        self,
        base_url,
        api_key,
        path: str = None,
        debug=False,
        label: str = None,
    ):
        if debug:
            _enable_debug_logging()

        if path:
            self._base_url = f"{base_url}/api/v1/users/{path}"
        else:
            self._base_url = f"{base_url}/api/v1/"

        _LOGGER.debug(f"generated base url: {self._base_url}")

        self._api_key = api_key
        self._caller_label = label or ""
        self._masked_key = _mask_api_key(api_key)
        self._headers = {"accept": "application/json", "Authorization": f"Bearer {self._api_key}"}

    async def _get_request(self, end_url: str):
        """Perform GET request to API endpoint, logging the call and its response."""
        request_url = urljoin(self._base_url, end_url)
        _log_request("GET", request_url, self._caller_label, self._masked_key)
        t0 = time.perf_counter()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{request_url}", headers=self._headers) as resp:
                    response = resp
                    responsetext = await resp.text()
        except Exception as exc:  # network error / timeout before a response arrived
            _log_failure(request_url, (time.perf_counter() - t0) * 1000.0, exc)
            raise

        _log_response(response.status, responsetext, (time.perf_counter() - t0) * 1000.0, request_url)
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

    async def get_todo(self, user_id) -> list[TodoItemResponse]:
        """Get the Canvas To-Do list for a specific user id.

        Calls GET /api/v1/users/{user_id}/todo. A concrete user id is required;
        passing 'self' is rejected so this never targets the authenticated user.
        """
        if user_id is None or str(user_id).strip().lower() == "self":
            raise ValueError("get_todo requires a concrete student user_id, not 'self'")
        parsed_json = await self._get_paginated(f"users/{user_id}/todo?per_page=50")
        return [TodoItemResponse(**resp) for resp in parsed_json]

    async def get_course_todo(self, course_id: int) -> list[TodoItemResponse]:
        """Get the Canvas To-Do list scoped to a single course."""
        parsed_json = await self._get_paginated(f"courses/{course_id}/todo?per_page=50")
        return [TodoItemResponse(**resp) for resp in parsed_json]
