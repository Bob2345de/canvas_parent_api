"""Base Model Definition."""
from typing import Optional
from pydantic.v1 import BaseModel, Field


class ObserveeResponse(BaseModel):
    """Observee Response Definition."""
    id: int
    name: str
    created_at: str
    sortable_name: str
    short_name: str
    observation_link_root_account: Optional[list[int]]


class CourseResponse(BaseModel):
    """Course Response Definition."""
    class Config:
        exclude = ['sis_course_id', 'uuid',
                   'integration_id', 'sis_import_id',
                   'workflow_state', 'account_id',
                   'root_account_id', 'grade_passback_setting',
                   'locale', 'total_students',
                   'default_view', 'needs_grading_count',
                   'apply_assignment_group_weights', 'permissions',
                   'is_public', 'is_public_to_auth_users',
                   'public_syllabus_to_auth', 'storage_quota_mb',
                   'storage_quota_used_mb', 'hide_final_grades',
                   'license', 'allow_student_assignment_edits',
                   'allow_wiki_comments', 'allow_student_forum_attachments',
                   'restrict_enrollments_to_course_dates', 'access_restricted_by_date',
                   'blueprint', 'blueprint_restrictions',
                   'blueprint_restrictions_by_object_type', 'template']
    id: int
    name: Optional[str]
    course_code: Optional[str]
    original_name: Optional[str]
    enrollment_term_id: Optional[int]
    grading_periods: Optional[list] = Field([None])
    grading_standard_id: Optional[int] = Field(None)
    created_at: Optional[str]
    start_at: Optional[str] = Field(None)
    end_at: Optional[str] = Field(None)
    enrollments: Optional[list] = Field([None])
    calendar: Optional[dict]
    syllabus_body: Optional[str]
    term: Optional[dict]
    course_progress: Optional[int]
    public_syllabus: Optional[bool]
    public_description: Optional[str]
    open_enrollment: Optional[bool]
    self_enrollment: Optional[bool]
    course_format: Optional[str]
    time_zone: Optional[str]


class AssignmentResponse(BaseModel):
    """Assignment Response Definition"""
    class Config:
        exclude = ['has_overrides', 'all_dates',
                   'html_url', 'submission_download_url',
                   'due_date_required',
                   'allowed_extensions', 'max_name_length',
                   'turnitin_enabled', 'vericite_enabled',
                   'turnitin_settings', 'grade_group_students_individually',
                   'external_tool_tag_attributes', 'peer_reviews',
                   'autoamtic_peer_reviews', 'peer_review_count',
                   'peer_reviews_assign_at', 'intra_group_peer_reviews',
                   'group_category_id', 'needs_grading_count',
                   'needs_grading_count_by_section', 'position',
                   'post_to_sis', 'integration_id',
                   'integration_data', 'submission_types',
                   'grading_type', 'grading_standard_id',
                   'published', 'unpublishable',
                   'only_visible_to_overrides', 'locked_for_user',
                   'locked_info', 'lock_explanation',
                   'anonymous_submissions', 'freeze_on_copy',
                   'frozen', 'frozen_attributes',
                   'use_rubric_for_grading', 'rubric_settings',
                   'assignment_visibility', 'overrides',
                   'omit_from_final_grade', 'moderated_grading',
                   'grader_count', 'final_grader_id',
                   'grader_comments_visible_to_graders',
                   'graders_anonymous_to_graders', 'anonymous_grading',
                   'post_manually', 'score_statistics',
                   'annotatable_attachment_id', 'anonymize_students',
                   'require_lockdown_browser', 'muted']
    id: int
    name: Optional[str]
    description: Optional[str] = Field(None)
    created_at: Optional[str]
    updated_at: Optional[str]
    due_at: Optional[str]
    lock_at: Optional[str]
    unlock_at: Optional[str]
    course_id: Optional[int]
    assignment_group_id: Optional[int] = Field(None)
    points_possible: Optional[float]
    has_submitted_submissions: Optional[bool]
    quiz_id: Optional[int]
    discussion_topic: Optional[dict]
    submission: Optional[dict]
    rubric: Optional[list] = Field([None])
    can_submit: Optional[bool]
    important_dates: Optional[bool]


class SubmissionResponse(BaseModel):
    """Submission Response Definition"""
    class Config:
        exclude = ['assignment', 'course',
                   'html_url', 'preview_url',
                   'submission_type', 'url',
                   'user_id', 'grader_id',
                   'user', 'assignment_visible',
                   'extra_attempts', 'anonymous_id',
                   'posted_at', 'read_status',
                   'redo_request']
    assignment_id: int
    attempt: Optional[int]
    body: Optional[str]
    grade: Optional[str]
    grade_matches_current_submission: Optional[bool]
    score: Optional[float]
    submission_comments: Optional[str]
    submitted_at: Optional[str]
    late: Optional[bool]
    excused: Optional[bool]
    missing: Optional[bool]
    late_policy_status: Optional[str]
    points_deducted: Optional[float]
    workflow_state: Optional[str]


class AnnouncementResponse(BaseModel):
    """Announcement Response Definition."""
    id: int
    title: Optional[str]
    message: Optional[str]
    posted_at: Optional[str]
    delayed_post_at: Optional[str]
    context_code: Optional[str]
    read_state: Optional[str]
    html_url: Optional[str] = Field(None)
    url: Optional[str] = Field(None)
    author: Optional[dict] = Field(None)


class CalendarEventResponse(BaseModel):
    """Calendar Event Response Definition."""
    id: int
    title: Optional[str]
    description: Optional[str]
    start_at: Optional[str]
    end_at: Optional[str]
    all_day: Optional[bool]
    location_name: Optional[str] = Field(None)
    location_address: Optional[str] = Field(None)
    context_code: Optional[str]
    context_name: Optional[str] = Field(None)
    type: Optional[str] = Field(None)
    html_url: Optional[str] = Field(None)
    hidden: Optional[bool] = Field(None)
    assignment: Optional[dict] = Field(None)


class AssignmentGroupResponse(BaseModel):
    """Assignment Group Response Definition."""
    id: int
    name: Optional[str]
    position: Optional[int]
    group_weight: Optional[float]
    rules: Optional[dict] = Field(None)
    assignments: Optional[list] = Field([None])


class TeacherResponse(BaseModel):
    """Teacher (Course User) Response Definition."""
    id: int
    name: Optional[str]
    sortable_name: Optional[str]
    short_name: Optional[str]
    email: Optional[str] = Field(None)
    avatar_url: Optional[str] = Field(None)
    bio: Optional[str] = Field(None)
    pronouns: Optional[str] = Field(None)


class ModuleResponse(BaseModel):
    """Module Response Definition."""
    id: int
    name: Optional[str]
    position: Optional[int]
    unlock_at: Optional[str]
    require_sequential_progress: Optional[bool]
    prerequisite_module_ids: Optional[list] = Field([None])
    state: Optional[str] = Field(None)
    completed_at: Optional[str] = Field(None)
    items_count: Optional[int]
    items: Optional[list] = Field(None)
    published: Optional[bool] = Field(None)


class TodoItemResponse(BaseModel):
    """To-Do Item Response Definition.

    Canvas returns to-do items without an 'id' field; the payload wraps either an
    assignment or a quiz, so every field is optional.
    """
    type: Optional[str] = Field(None)
    assignment: Optional[dict] = Field(None)
    quiz: Optional[dict] = Field(None)
    ignore: Optional[str] = Field(None)
    ignore_permanently: Optional[str] = Field(None)
    html_url: Optional[str] = Field(None)
    needs_grading_count: Optional[int] = Field(None)
    context_type: Optional[str] = Field(None)
    course_id: Optional[int] = Field(None)
    group_id: Optional[int] = Field(None)
    context_name: Optional[str] = Field(None)
    visible_in_planner: Optional[bool] = Field(None)


class PlannerItemResponse(BaseModel):
    """Planner Item Response Definition.

    GET /api/v1/users/:user_id/planner/items returns flattened items where the
    human-readable name lives under ``title`` and the date under ``date``
    (unlike the calendar endpoint's start_at/title). Every field is optional
    because a planner item can represent an assignment, quiz, discussion,
    announcement, page or calendar event.
    """
    context_code: Optional[str] = Field(None)
    context_name: Optional[str] = Field(None)
    course_id: Optional[int] = Field(None)
    group_id: Optional[int] = Field(None)
    type: Optional[str] = Field(None)
    date: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    points_possible: Optional[float] = Field(None)
    html_url: Optional[str] = Field(None)
    planner_override: Optional[dict] = Field(None)
    submissions: Optional[dict] = Field(None)
    new_activity: Optional[bool] = Field(None)


class ActivityStreamItemResponse(BaseModel):
    """Activity Stream Item Response Definition."""
    id: int
    title: Optional[str]
    message: Optional[str]
    type: Optional[str]
    read_state: Optional[bool] = Field(None)
    context_type: Optional[str] = Field(None)
    course_id: Optional[int] = Field(None)
    group_id: Optional[int] = Field(None)
    created_at: Optional[str]
    updated_at: Optional[str]
    html_url: Optional[str] = Field(None)
