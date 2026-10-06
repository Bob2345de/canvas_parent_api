# Changelog

[2026-10-06 15:45] - Calendar tool now uses the Planner endpoint (planner/items)
Summary: The calendar tool (canvas_get_calendar_events) now fetches each child's schedule from GET /api/v1/users/:user_id/planner/items (Canvas "My Planner" feed) instead of the calendar_events endpoint, with start_date = today and end_date = today + days_ahead. Added library support: client.planner_items(user_id, start_date, end_date, context_codes, observed_user_id, filter) with the new PlannerItem model (name/date/type/context_name/points/html_url/submitted/marked_complete). Library 0.0.28 -> 0.0.29, tool 0.3.3 -> 0.3.4.

Files changed:

src/canvas_parent_api/models/base.py — added PlannerItemResponse (context_code, context_name, course_id, group_id, type, date, title, points_possible, html_url, planner_override, submissions, new_activity).

src/canvas_parent_api/models/planner_item.py — new PlannerItem wrapper with name/date/due_at/type/context_name/points_possible/html_url and submitted/marked_complete conveniences.

src/canvas_parent_api/canvas_api_client.py — added get_planner_items() building users/{user_id}/planner/items?per_page=50&start_date=...&end_date=...&context_codes[]=...&observed_user_id=...&filter=...; imported PlannerItemResponse.

src/canvas_parent_api/canvas.py — added public async planner_items(...) method; imported PlannerItem.

Canvas Parent Monitor.json — canvas_get_calendar_events now calls client.planner_items(student.id, start_date, end_date) and renders name/type/context/points/state/link lines; docstring updated; version 0.3.3 -> 0.3.4.

setup.py, pyproject.toml — library version 0.0.28 -> 0.0.29.

README.md — patch note for 0.0.29 (Planner API).

build_deploy.ps1 — wheel verification now also checks for get_planner_items and models/planner_item.py.

[2026-10-06 15:20] - Added build_deploy.ps1 one-command rebuild script
Summary: New PowerShell script that cleans stale build/ + egg-info + dist artifacts, builds a fresh wheel from src/, verifies the wheel really contains the current code (courses() enrollment_state param, label kwarg, per-call logger), and optionally deploys it into the Open WebUI container and runtime-verifies the installed signature. Run `pwsh build_deploy.ps1 [-Container name] [-NoDeploy]`.

Files changed:

build_deploy.ps1 — new script (clean -> build -> verify -> deploy -> verify installed code).

[2026-10-06 15:00] - Removed stale tracked build/ artifacts (root cause of stale library installs)
Summary: `build/lib/canvas_parent_api/*` was committed to git and contained 0.0.24-era code (Canvas.courses() without enrollment_state, no request/response logging). Anything installed from this directory or from GitHub master.zip (which includes build/) therefore ran old code even when version metadata said 0.0.28, causing "Canvas.courses() got an unexpected keyword argument 'enrollment_state'". Removed build/ from the repo and git history onwards, added build/ to .gitignore, and built a verified-clean wheel (canvas_parent_api-0.0.28-py3-none-any.whl) from src/ that contains courses(..., enrollment_state), the label kwarg, and the per-call logger.

Files changed:

.gitignore — added build/ and src/canvas_parent_api.egg-info/ so build artifacts can't be committed again.

build/lib/canvas_parent_api/... (18 files) — deleted from the repo; these stale artifacts were the source of the wrong-code installs.

canvas_parent_api-0.0.28-py3-none-any.whl — built fresh into dist/ (gitignored) from src/ and verified to contain the current code.

REINSTALL REQUIRED IN CONTAINER: docker cp dist/canvas_parent_api-0.0.28-py3-none-any.whl open-webui:/tmp/ && docker exec open-webui pip install --force-reinstall /tmp/canvas_parent_api-0.0.28-py3-none-any.whl, then verify with inspect.signature(Canvas.courses). If the tool re-installs from the GitHub master.zip (tool requirements line), push these changes to GitHub first so the zip no longer contains build/.

[2026-10-06 14:40] - Fallback when installed library lacks enrollment_state on courses()
Summary: Fixed "Canvas.courses() got an unexpected keyword argument 'enrollment_state'" (container running canvas_parent_api < 0.0.25). _get_filtered_courses now checks via inspect.signature whether the installed Canvas.courses() accepts enrollment_state and calls courses(student.id) without it when not supported. Tool version 0.3.2 -> 0.3.3. Container still needs the library updated to 0.0.28 for full functionality + request/response logging.

Files changed:

Canvas Parent Monitor.json — added _courses_supports_enrollment_state() helper; _get_filtered_courses falls back to courses(student.id) on older libraries. Version 0.3.2 -> 0.3.3.

[2026-10-06 14:20] - Backward-compatible label in tool client factory
Summary: Fixed "Canvas.__init__() got an unexpected keyword argument 'label'" seen when the Open WebUI container still runs canvas_parent_api < 0.0.28. The tool now checks whether the installed library accepts the label kwarg and falls back to Canvas(base_url, token) if not, so tools keep working until the container's library is updated; tool version 0.3.1 -> 0.3.2.

Files changed:

Canvas Parent Monitor.json — added _canvas_supports_label() (inspect.signature check) and _new_canvas_client(); _get_client uses them so label= is only passed when supported by the installed library. Version 0.3.1 -> 0.3.2. To get the full logging feature (caller labels + request/response log), update the library inside the container to 0.0.28.

[2026-10-06 13:15] - Per-call Canvas API request/response logging
Summary: The backend API client now logs every HTTP request it makes to the Canvas API — the request (method, full URL, masked token, caller label) and the response (status, elapsed time, body) — with timestamps, to a text file. Default location is /app/backend/data/canvas_api.log (the Open WebUI data dir, volume-mounted to the host so it is reachable both inside the container and from the host); configurable via CANVAS_API_LOG_FILE and CANVAS_API_LOG_MAX_BODY. The tool passes a caller label (child name or "parent") so entries identify which key made the call. Library 0.0.27 -> 0.0.28, tool 0.3.0 -> 0.3.1.

Files changed:

src/canvas_parent_api/canvas_api_client.py — added a file-based call logger (path resolution with fallbacks, thread-safe flushed writes, masked token display, response body truncation) and wired _get_request to log REQUEST / RESPONSE / ERROR lines with timestamps; __init__ accepts label for call tagging.

src/canvas_parent_api/canvas.py — Canvas.__init__ now accepts label and threads it through to CanvasApiClient.

Canvas Parent Monitor.json — _get_client gains a label param; parent client is labelled "parent" and child clients are labelled with the child's name.

setup.py, pyproject.toml — library version 0.0.27 -> 0.0.28 so Open WebUI installs a distinct build.

README.md — patch note for 0.0.28 describing the API call log and env vars.

[2026-10-06 12:00] - Per-child Canvas API tokens
Summary: Added a CHILD_1_TOKEN / CHILD_2_TOKEN / CHILD_3_TOKEN valve next to each child's name and re-routed every per-child request (courses, assignments, grades, announcements, calendar events, assignment details, teachers, modules, syllabus, to-do) to a Canvas client built from that child's OWN token. The parent token (CANVAS_API_TOKEN) is now used only for looking up which children are linked to the account (observees → user ids/names) and for get_recent_activity, as those are the only functions that require the parent key. Clients are cached per (base_url, token); a missing child token produces a clear per-child error instead of calling the API.

Files changed:

Canvas Parent Monitor.json — added CHILD_1_TOKEN, CHILD_2_TOKEN, CHILD_3_TOKEN password valves; replaced the single cached client with a per-token client cache (_get_client(token), _get_parent_client, _child_slots, _token_for_student, _client_for_student); _get_filtered_students and get_recent_activity now use the parent client, while _get_filtered_courses, _process_all_assignments, canvas_get_announcements, canvas_get_calendar_events, get_assignment_details, get_grades_by_category, get_course_syllabus, get_teachers, get_module_progress and canvas_get_todo resolve each child's own client via _client_for_student. Tool version 0.2.5 -> 0.3.0.

[2026-09-03 12:30] - canvas_get_todo now calls GET /users/{student_id}/todo directly (no courses()/enrollment_state)
Summary: Fixed the persistent "Canvas.courses() got an unexpected keyword argument 'enrollment_state'" crash by removing the to-do tool's dependency on the course list entirely. canvas_get_todo now resolves each child via observees and calls client.todo(student.id) — i.e. GET /api/v1/users/{student_id}/todo with the child's own Canvas user id — so it no longer touches courses(), enrollment_state, or the per-course /courses/:id/todo endpoint. The library todo() was tightened to require a concrete user id and to reject 'self' so the code can never hit /users/self/todo. Verified with an end-to-end simulation that courses() is never called and the correct student ids are used.

Files changed:

Canvas Parent Monitor.json — rewrote canvas_get_todo to call client.todo(student.id) (GET /users/{student_id}/todo) and group/sort results in memory via a new _todo_course_label helper; dropped all _get_filtered_courses/course_todo/enrollment_state usage from this tool path; course_name is now an in-memory filter on each item's course context. Tool version 0.2.4 -> 0.2.5; requirements URL back to master.zip.

src/canvas_parent_api/canvas.py — todo(user_id) no longer defaults to 'self'; requires an explicit user id.

src/canvas_parent_api/canvas_api_client.py — get_todo(user_id) raises ValueError if user_id is None or 'self', guaranteeing the client never requests /users/self/todo.

pyproject.toml, setup.py — library version 0.0.26 -> 0.0.27.

README.md — documented that todo(user_id) requires a concrete student id (self rejected); added 0.0.27 patch notes.

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
