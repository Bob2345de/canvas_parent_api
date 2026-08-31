# Changelog

[2026-08-31 13:00] - Rewrote Canvas Parent Monitor Open WebUI tool with 16 self-explanatory tool methods
Summary: Rebuilt the Open WebUI tool to use the newly added library endpoints (announcements, calendar events, assignment details/feedback, assignment groups, syllabus, teachers, modules, activity stream) and improved it generally: LLM-friendly docstrings with example questions, HTML-to-text conversion, course_name filtering, error aggregation, client cache invalidation on valve change, and a combined daily summary. Also exposed assignment_group_id on the Assignment model (needed for grades-by-category).

Files changed:

Canvas Parent Monitor.json — full rewrite; now 16 tool methods: list_children, list_courses, get_current_grades, get_upcoming_assignments, get_missing_assignments, get_completed_assignments, get_recent_grades, get_announcements, get_calendar_events, get_assignment_details, get_grades_by_category, get_course_syllabus, get_teachers, get_module_progress, get_recent_activity, get_daily_summary

src/canvas_parent_api/models/base.py — AssignmentResponse now includes assignment_group_id (removed from exclude list)

src/canvas_parent_api/models/assignment.py — added assignment_group_id property

[2026-08-31 12:00] - Added 8 new Canvas Parent API endpoints
Summary: Added support for Announcements, Calendar Events, single Assignment details, Assignment Groups (grade categories), single Course details (syllabus), Teachers, Modules (progress), and Activity Stream, following the existing 4-layer pattern (pydantic response model, DataModel wrapper, API client method, Canvas public method). Bumped version to 0.0.24. Attendance (Roll Call) was excluded because it is not part of the public Canvas REST API.

Files changed:

src/canvas_parent_api/models/base.py — added AnnouncementResponse, CalendarEventResponse, AssignmentGroupResponse, TeacherResponse, ModuleResponse, ActivityStreamItemResponse pydantic models

src/canvas_parent_api/models/announcement.py — new Announcement DataModel

src/canvas_parent_api/models/calendar_event.py — new CalendarEvent DataModel

src/canvas_parent_api/models/assignment_group.py — new AssignmentGroup DataModel

src/canvas_parent_api/models/teacher.py — new Teacher DataModel

src/canvas_parent_api/models/module.py — new Module DataModel

src/canvas_parent_api/models/activity_stream_item.py — new ActivityStreamItem DataModel

src/canvas_parent_api/canvas_api_client.py — added _get_paginated helper and get_announcements, get_calendar_events, get_assignment, get_assignment_groups, get_course, get_teachers, get_modules, get_activity_stream methods

src/canvas_parent_api/canvas.py — added announcements, calendar_events, assignment, assignment_groups, course, teachers, modules, activity_stream public async methods

README.md — documented new object types, added Available Methods section, patch notes for 0.0.24, and Roll Call limitation note

pyproject.toml — version bump 0.0.23 -> 0.0.24

setup.py — version bump 0.0.23 -> 0.0.24
