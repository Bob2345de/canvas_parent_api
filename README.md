# Canvas Parent API
This is an async wrapper for the [Canvas API](https://canvas.instructure.com/doc/api/) from Instructure.  There are a few types of objects this will retrieve based on the assumption that you are a parent with students enrolled with Canvas.  

The types of objects that can be returned include:
 - Observees (Students)
 - Courses
 - Assignments
 - Submissions
 - Announcements
 - Calendar Events
 - Assignment Groups (grade categories)
 - Teachers
 - Modules (with progress)
 - Activity Stream (recent activity feed)

This module is provided for use with the Home Assistant custom integration [Canvas](https://github.com/schwartzpub/canvas_hassio) however it could be useful as a standalone module for your own projects as well.

## Installing
To install the module use:
```python
python3 -m pip install canvas-parent-api
```

### Get API Token
If you are a parent, you will have a Canvas Parent account.  To get an API token, you must sign into the Canvas Parent application from a web browser.  This is typically using: https://<yourdistrict>.instructure.com/login/canvas

Once you have signed into your account, navigate to Account > Settings.

Under "Approved Integrations" click "+ New Access Token" to create a new API Token.

Enter a Purpose and Expiration date (blank for no expiration).

Be sure to save your API token, as you will have to generate a new token if this is lost.

### Usage
Example usage to get students, printing names:
```python
import asyncio
from canvas_parent_api import Canvas

base_url = "https://school.instructure.com"
api_token = "randomstringthatisntreallyatoken"

async def get_students():
	client = Canvas(f"{base_url}",f"{api_token}")
	return await client.observees()

students = asyncio.run(get_students())

for student in students:
	print(student.name)
```

### Available Methods
All methods are async and return model objects with properties matching the Canvas API response fields (each object supports `.as_dict()` and `.tojson()`).

```python
client = Canvas(base_url, api_token)

# Students
await client.observees()

# Courses for a student
await client.courses(student_id)

# Single course incl. syllabus_body / public_description
await client.course(course_id)

# Assignments for a student in a course
await client.assignments(student_id, course_id)

# Single assignment with submission details (grade, feedback via rubric/submission)
await client.assignment(course_id, assignment_id)

# Submissions for a student in a course
await client.submissions(student_id, course_id)

# Recent teacher announcements for a course (default: last 7 days)
await client.announcements(course_id, days_back=7)

# Upcoming calendar events for a student (default: next 14 days)
# event_type can be "event" or "assignment"
await client.calendar_events(student_id, days_ahead=14, event_type="event")

# Assignment groups (grade categories such as Homework, Quizzes, Tests)
await client.assignment_groups(course_id)

# Teachers for a course (name, email, avatar)
await client.teachers(course_id)

# Modules with items and per-student completion state
await client.modules(course_id, student_id)

# Recent activity feed for the current (parent) user
await client.activity_stream(only_active_courses=True)
```

Note: Attendance (Roll Call) is not available through the public Canvas REST API (it is a separate LTI tool), so it is not supported by this module.

### Patch Notes

 - 0.0.24:
	- Added Announcements, Calendar Events, single Assignment details, Assignment Groups, single Course (syllabus), Teachers, Modules (progress), and Activity Stream endpoints

 - 0.0.12:
    - Added pagination support to automatically paginate to end of available requests

 - 0.0.9:
	- Added Submissions