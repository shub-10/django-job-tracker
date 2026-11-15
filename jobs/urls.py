from django.urls import path
from .views import (
    health_check,
    signup,
    login_user,
    create_job_post,
    get_job_posts,
    apply_for_job,
    get_my_applications,
    get_job_posts_by_me,
    get_applications_for_job_post,
    update_application_status,
)

urlpatterns = [
    path("api/health/", health_check, name="health"),
    path("api/auth/signup", signup, name="signup"),
    path("api/auth/login", login_user, name="login"),
    path("api/jobs", get_job_posts, name="get_job_posts"),
    path("api/jobs/<int:job_post_id>/apply", apply_for_job, name="apply_for_job"),
    path("api/user/myapplications", get_my_applications, name="get_my_applications"),
    path("api/jobs/create", create_job_post, name="create_job_post"),
    path("api/posted/jobs", get_job_posts_by_me, name="get_job_posts_by_me"),
    path(
        "api/<int:job_post_id>/applications",
        get_applications_for_job_post,
        name="get_applications_for_job_post",
    ),
    path(
        "api/<int:application_id>/update-status",
        update_application_status,
        name="update_application_status",
    ),
]
