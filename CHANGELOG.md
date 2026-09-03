# Changelog

[2026-09-03 11:15] - Pinned Open WebUI tool to a commit archive to force a fresh library install
Summary: Fixed the runtime error "Canvas.courses() got an unexpected keyword argument 'enrollment_state'" (and the follow-on missing course_todo/todo methods), which was caused by Open WebUI serving a STALE cached install of canvas_parent_api from the unchanging master.zip URL even though origin/master already contained the 0.0.26 code. Changed the requirements URL from the branch archive (master.zip) to a commit-pinned archive so pip/Open WebUI treats it as a new dependency and re-downloads the current build; verified the commit archive resolves to a valid zip.

Files changed:

Canvas Parent Monitor.json — requirements line now points at https://github.com/Bob2345de/canvas_parent_api/archive/f6ea7f3d468add038e9f891e41893fa7886cc82e.zip (commit-pinned) instead of the cached refs/heads/master.zip; tool version 0.2.3 -> 0.2.4. No tool logic changed; the source already had enrollment_state, todo() and course_todo().

[2026-09-03 10:00] - Added Canvas To-Do List support (global and course-specific) plus a child-name tool
Summary: Added the two Canvas To-Do endpoints the user requested - the global list across all courses (GET /api/v1/users/:user_id/todo) and the course-specific list (GET /api/v1/courses/:course_id/todo) - following the existing 4-layer pattern, and exposed them to the LLM through a new canvas_get_todo(child_name, course_name) Open WebUI tool that shows each child's outstanding assignments/quizzes grouped by course and ordered by due date.

Files changed:

src/canvas_parent_api/models/base.py — added TodoItemResponse pydantic model (all optional fields since Canvas to-do items wrap either an assignment or a quiz and carry no id).

src/canvas_parent_api/models/todo_item.py — new TodoItem DataModel with convenience name/due_at/points_possible/course_id properties derived from the nested assignment or quiz payload.

src/canvas_parent_api/canvas_api_client.py — imported TodoItemResponse and added get_todo(user_id="self") and get_course_todo(course_id), both paginated.

src/canvas_parent_api/canvas.py — imported TodoItem and added public async todo(user_id="self") and course_todo(course_id) methods.

Canvas Parent Monitor.json — added canvas_get_todo(child_name, course_name) tool method (reads course_todo per current course, groups by course, sorts by due date); header description now mentions the to-do list; version 0.2.2 -> 0.2.3.

pyproject.toml, setup.py — library version 0.0.25 -> 0.0.26.

README.md — added To-Do Items to the object list, documented client.todo()/client.course_todo() in Available Methods, and added 0.0.26 patch notes.

[2026-09-02 17:30] - Fixed courses from previous school years appearing in "what courses does X have"
Summary: GET /api/v1/users/:user_id/courses was called without an enrollment_state filter, and Canvas defaults to returning both active AND completed (concluded) enrollments, so last year's classes came back alongside the current ones. get_courses now sends enrollment_state=active by default, and a new canvas_get_past_courses tool method exposes the history separately so the LLM can still answer "what did she take last year?". Also fixed a latent pagination bug where only the first two pages were ever fetched.

Files changed:

src/canvas_parent_api/canvas_api_client.py — get_courses gained an enrollment_state parameter (default "active") appended to the query string; pass None for the old Canvas default. get_courses, get_observees, get_assignments and get_submissions now use the existing _get_paginated helper instead of manually fetching only page 1 plus one next page, which silently truncated results at 100 items.

src/canvas_parent_api/canvas.py — Canvas.courses(student_id, enrollment_state="active") threads the new argument through to the API client.

Canvas Parent Monitor.json — _get_filtered_courses gained an enrollment_state argument defaulting to "active", so all existing tool methods now see only current-year courses. Added new canvas_get_past_courses(child_name, school_year) tool method that lists concluded courses grouped by term with final grades, with an optional school_year substring filter. list_courses docstring now states it covers only the current school year and points at canvas_get_past_courses for history. Header description mentions past course history; version 0.2.1 -> 0.2.2.

pyproject.toml, setup.py — library version 0.0.24 -> 0.0.25 so Open WebUI installs a distinct build from the GitHub archive URL.

README.md — documented the enrollment_state argument on client.courses() and added 0.0.25 patch notes.

[2026-09-02 15:30] - Renamed calendar tool method to canvas_get_calendar_events to avoid Exchange tool collision
Summary: Renamed the Open WebUI tool method get_calendar_events to canvas_get_calendar_events because a separate Exchange/Outlook tool already exposes get_calendar_events, which made it ambiguous for the LLM to pick the right one. The docstring now states explicitly that this tool returns SCHOOL calendar data from Canvas for the children Niclas and Annabelle, lists example questions using their names, and adds a DO NOT USE note pointing personal/work calendar requests at the Exchange tool instead.

Files changed:

Canvas Parent Monitor.json — renamed get_calendar_events to canvas_get_calendar_events; rewrote its docstring with Niclas/Annabelle school-calendar scope, positive/negative usage guidance, and child_name values; header description now says "school data for Niclas and Annabelle" and "school calendar events"; version 0.2.0 -> 0.2.1. The internal client.calendar_events(...) library call was intentionally left unchanged.

[2026-08-31 15:00] - Fixed "can't compare offset-naive and offset-aware datetimes" in calendar/date handling
Summary: Tools._parse_date in the Open WebUI tool could return a timezone-naive datetime when Canvas sent a date string without a UTC offset (e.g., date-only values for all-day calendar events), which then blew up when compared against timezone-aware datetime.now(timezone.utc). The parser now assumes UTC and attaches tzinfo to any naive result, so all date comparisons (calendar events, upcoming/missing/completed assignments, recent grades, activity stream) are safe.

Files changed:

Canvas Parent Monitor.json — _parse_date now normalizes naive parsed datetimes to timezone-aware UTC

[2026-08-31 14:00] - Pointed Open WebUI tool requirements at the GitHub fork
Summary: Changed the tool header requirements line from the PyPI package (canvas-parent-api>=0.0.24, which resolves to the official upstream release) to a PEP 508 direct URL that installs the fork from GitHub, so Open WebUI pulls this repo's version with the new endpoints.

Files changed:

Canvas Parent Monitor.json — requirements line now: canvas_parent_api @ https://github.com/Bob2345de/canvas_parent_api/archive/refs/heads/master.zip

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
