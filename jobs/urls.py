from django.urls import path
from .views import health_check, signup, loginUser, createJobPost, getJobPosts, getJobPostById

urlpatterns = [
    path("api/health/", health_check, name="health"),
    path("api/auth/signup", signup, name="signup"),
    path("api/auth/login", loginUser, name="login"),
    path("api/jobs", getJobPosts, name="getJobPosts"),
    path("api/jobs/create", createJobPost, name="createJobPost"),
    path("api/jobs/<int:jobPostId>/apply", getJobPostById, name="getJobPostById"),
]
