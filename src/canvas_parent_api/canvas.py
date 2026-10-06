"""Base Canvas Class."""
import logging

from datetime import datetime, timedelta, timezone

from canvas_parent_api.models.submission import Submission

from .models.observee import Observee
from .models.course import Course
from .models.assignment import Assignment
from .models.announcement import Announcement
from .models.calendar_event import CalendarEvent
from .models.assignment_group import AssignmentGroup
from .models.teacher import Teacher
from .models.module import Module
from .models.activity_stream_item import ActivityStreamItem
from .models.todo_item import TodoItem
from .models.planner_item import PlannerItem
from .canvas_api_client import CanvasApiClient

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)


class Canvas():
    """Define Canvas Class."""
    def __init__(
        self,
        base_url,
        api_key,
        path: str = None,
        debug=False,
        label: str = None,
    ):
        self._api_client = CanvasApiClient(base_url, api_key, path, debug, label)

        if debug:
            _LOGGER.setLevel(logging.DEBUG)

    async def observees(self) -> list[Observee]:
        """Get Observees."""
        observeesresp = await self._api_client.get_observees()
        observees = [Observee(response) for response in observeesresp]
        return observees

    async def courses(self, student_id, enrollment_state: str = "active") -> list[Course]:
        """Get Courses: must supply student id.

        Defaults to currently active enrollments only. Canvas would otherwise also
        return concluded enrollments, i.e. courses from previous school years.
        Pass enrollment_state='completed' for past courses, or None for everything.
        """
        coursesresp = await self._api_client.get_courses(student_id, enrollment_state)
        courses = [Course(response) for response in coursesresp]
        return courses

    async def assignments(self, student_id, course_id) -> list[Assignment]:
        """Get Assignments: must supply student id and course id."""
        assignmentsresp = await self._api_client.get_assignments(student_id, course_id)
        assignments = [Assignment(response) for response in assignmentsresp]
        return assignments

    async def submissions(self, student_id, course_id) -> list[Submission]:
        """Get Submissions: must supply student id and course id."""
        submissionsresp = await self._api_client.get_submissions(student_id, course_id)
        submissions = [Submission(response) for response in submissionsresp]
        return submissions

    async def announcements(self, course_id, days_back: int = 7) -> list[Announcement]:
        """Get Announcements: must supply course id, optionally days back to search."""
        now = datetime.now(timezone.utc)
        start_date = (now - timedelta(days=days_back)).strftime("%Y-%m-%d")
        end_date = now.strftime("%Y-%m-%d")
        announcementsresp = await self._api_client.get_announcements(course_id, start_date, end_date)
        announcements = [Announcement(response) for response in announcementsresp]
        return announcements

    async def calendar_events(self, student_id, days_ahead: int = 14, event_type: str = "event") -> list[CalendarEvent]:
        """Get Calendar Events: must supply student id, optionally days ahead and event type ('event' or 'assignment')."""
        now = datetime.now(timezone.utc)
        start_date = now.strftime("%Y-%m-%d")
        end_date = (now + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        eventsresp = await self._api_client.get_calendar_events(student_id, start_date, end_date, event_type)
        events = [CalendarEvent(response) for response in eventsresp]
        return events

    async def assignment(self, course_id, assignment_id) -> Assignment:
        """Get Assignment Details: must supply course id and assignment id."""
        assignmentresp = await self._api_client.get_assignment(course_id, assignment_id)
        return Assignment(assignmentresp)

    async def assignment_groups(self, course_id) -> list[AssignmentGroup]:
        """Get Assignment Groups (grade categories): must supply course id."""
        groupsresp = await self._api_client.get_assignment_groups(course_id)
        groups = [AssignmentGroup(response) for response in groupsresp]
        return groups

    async def course(self, course_id) -> Course:
        """Get Course Details (including syllabus): must supply course id."""
        courseresp = await self._api_client.get_course(course_id)
        return Course(courseresp)

    async def teachers(self, course_id) -> list[Teacher]:
        """Get Teachers: must supply course id."""
        teachersresp = await self._api_client.get_teachers(course_id)
        teachers = [Teacher(response) for response in teachersresp]
        return teachers

    async def modules(self, course_id, student_id=None) -> list[Module]:
        """Get Modules with progress: must supply course id, optionally student id for completion state."""
        modulesresp = await self._api_client.get_modules(course_id, student_id)
        modules = [Module(response) for response in modulesresp]
        return modules

    async def activity_stream(self, only_active_courses: bool = True) -> list[ActivityStreamItem]:
        """Get Recent Activity Stream for the current (parent) user."""
        activityresp = await self._api_client.get_activity_stream(only_active_courses)
        activity = [ActivityStreamItem(response) for response in activityresp]
        return activity

    async def todo(self, user_id) -> list[TodoItem]:
        """Get the To-Do list (across all courses) for a specific user.

        A concrete Canvas user id is required (e.g. a student's id); this method
        deliberately does not accept 'self' so callers always target a specific
        student rather than the authenticated account.
        """
        todoresp = await self._api_client.get_todo(user_id)
        return [TodoItem(response) for response in todoresp]

    async def course_todo(self, course_id) -> list[TodoItem]:
        """Get the To-Do list scoped to a single course: must supply course id."""
        todoresp = await self._api_client.get_course_todo(course_id)
        return [TodoItem(response) for response in todoresp]

    async def planner_items(
        self,
        user_id,
        start_date: str = None,
        end_date: str = None,
        context_codes: list = None,
        observed_user_id: int = None,
        filter: str = None,
    ) -> list[PlannerItem]:
        """Get Canvas Planner items for a student: must supply student id.

        Calls GET /api/v1/users/{user_id}/planner/items — the data source for the
        Canvas "My Planner" dashboard. Usable as a calendar feed for a child.

        :param user_id: Canvas user id of the student.
        :param start_date: Only return items starting from this date
            (yyyy-mm-dd or ISO 8601 YYYY-MM-DDTHH:MM:SSZ).
        :param end_date: Only return items up to this date.
        :param context_codes: Optional list like ["course_42", "group_123"] to
            limit items to those courses/groups; defaults to all of the user's.
        :param observed_user_id: Return planner items for the given observed
            user (must be accompanied by context_codes[]).
        :param filter: "new_activity", "incomplete_items" or "complete_items".
        """
        itemsresp = await self._api_client.get_planner_items(
            user_id, start_date, end_date, context_codes, observed_user_id, filter
        )
        return [PlannerItem(response) for response in itemsresp]
