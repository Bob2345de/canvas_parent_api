"""Ad-hoc test: verify the Canvas Parent Monitor routes each call to the right token.

Loads the tool source (stored in the .json file), stubs out the Canvas client and
the canvas_parent_api import, then checks that observees()/activity_stream() use the
PARENT token and all per-child calls use that child's OWN token.
"""
import asyncio
import io
import sys
import types


# ---- Stub the canvas_parent_api.Canvas dependency ---------------------------
CALLS = []  # (token, method, args)


class FakeStudent:
    def __init__(self, sid, name):
        self.id = sid
        self.name = name
        self.short_name = name
        self.sortable_name = name


class FakeCourse:
    def __init__(self, cid, name):
        self.id = cid
        self.name = name
        self.course_code = name
        self.enrollments = []
        self.syllabus_body = None
        self.public_description = None
        self.term = None


class FakeCanvas:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    async def observees(self):
        CALLS.append((self.token, "observees", ()))
        return [FakeStudent(101, "Niclas"), FakeStudent(202, "Annabelle")]

    async def courses(self, student_id, enrollment_state="active"):
        CALLS.append((self.token, "courses", (student_id, enrollment_state)))
        return [FakeCourse(student_id * 10 + 1, f"Math-{student_id}")]

    async def calendar_events(self, student_id, days_ahead=14):
        CALLS.append((self.token, "calendar_events", (student_id,)))
        return []

    async def todo(self, student_id):
        CALLS.append((self.token, "todo", (student_id,)))
        return []

    async def teachers(self, course_id):
        CALLS.append((self.token, "teachers", (course_id,)))
        return []

    async def activity_stream(self, only_active_courses=True):
        CALLS.append((self.token, "activity_stream", ()))
        return []


fake_module = types.ModuleType("canvas_parent_api")
fake_module.Canvas = FakeCanvas
sys.modules["canvas_parent_api"] = fake_module


# ---- Load the tool source (from the .json file) -----------------------------
SRC_PATH = r"c:\Users\Me\Documents\Canvas Client API\canvas_parent_api\Canvas Parent Monitor.json"
src = io.open(SRC_PATH, encoding="utf-8").read()
ns = {}
exec(compile(src, SRC_PATH, "exec"), ns)
Tools = ns["Tools"]


def make_tool():
    t = Tools()
    t.valves.CANVAS_BASE_URL = "https://school.instructure.com"
    t.valves.CANVAS_API_TOKEN = "PARENT_TOKEN"
    t.valves.CHILD_1_NAME = "Niclas"
    t.valves.CHILD_1_TOKEN = "NICLAS_TOKEN"
    t.valves.CHILD_2_NAME = "Annabelle"
    t.valves.CHILD_2_TOKEN = "ANNABELLE_TOKEN"
    return t


async def main():
    failures = []

    # 1) list_children -> parent token only
    CALLS.clear()
    t = make_tool()
    await t.list_children()
    assert CALLS == [("PARENT_TOKEN", "observees", ())], CALLS
    print("list_children uses parent token only:", CALLS)

    # 2) list_courses -> observees on parent, courses on each child's token
    CALLS.clear()
    t = make_tool()
    await t.list_courses()
    tokens_by_method = {}
    for tok, method, args in CALLS:
        tokens_by_method.setdefault(method, set()).add(tok)
    assert tokens_by_method["observees"] == {"PARENT_TOKEN"}, tokens_by_method
    assert tokens_by_method["courses"] == {"NICLAS_TOKEN", "ANNABELLE_TOKEN"}, tokens_by_method
    print("list_courses: observees=parent, courses=child tokens OK")

    # 3) calendar events use child tokens
    CALLS.clear()
    t = make_tool()
    await t.canvas_get_calendar_events()
    cal = {tok for tok, m, a in CALLS if m == "calendar_events"}
    assert cal == {"NICLAS_TOKEN", "ANNABELLE_TOKEN"}, CALLS
    print("calendar_events uses child tokens OK")

    # 4) recent activity uses parent token
    CALLS.clear()
    t = make_tool()
    await t.get_recent_activity()
    assert CALLS == [("PARENT_TOKEN", "activity_stream", ())], CALLS
    print("get_recent_activity uses parent token OK")

    # 5) filtering to one child uses only that child's token for data calls
    CALLS.clear()
    t = make_tool()
    await t.list_courses(child_name="Annabelle")
    data_tokens = {tok for tok, m, a in CALLS if m == "courses"}
    assert data_tokens == {"ANNABELLE_TOKEN"}, CALLS
    print("single-child filter uses only that child token OK")

    # 6) missing child token -> clear error, no data call
    CALLS.clear()
    t = make_tool()
    t.valves.CHILD_2_TOKEN = ""  # Annabelle has no token
    out = await t.list_courses(child_name="Annabelle")
    assert "No Canvas API token is configured for Annabelle" in out, out
    assert not any(m == "courses" for tok, m, a in CALLS), CALLS
    print("missing child token produces error + no data call OK")

    print("\nALL CHECKS PASSED")
    if failures:
        raise SystemExit("FAILURES: " + "; ".join(failures))


asyncio.run(main())
