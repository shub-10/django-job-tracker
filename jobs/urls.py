from django.urls import path
from .views import health_check, signup, loginUser, createJobPost, getJobPosts, applyForJob, getMyApplications, getJobPostByMe, getApplicationsForJobPost, updateApplicationStatus

urlpatterns = [
    path("api/health/", health_check, name="health"),
    path("api/auth/signup", signup, name="signup"),
    path("api/auth/login", loginUser, name="login"),
    path("api/jobs", getJobPosts, name="getJobPosts"),
    path("api/jobs/<int:jobPostId>/apply", applyForJob, name="applyForJob"),
    path("api/user/myapplications", getMyApplications, name="getMyApplications"),
    path("api/jobs/create", createJobPost, name="createJobPost"),
    path("api/posted/jobs", getJobPostByMe, name="getJobPostByMe"),
    path("api/<int:jobPostId>/applications", getApplicationsForJobPost, name="getApplicationsForJobPost"),
    path("api/<int:applicationId>/update-status", updateApplicationStatus, name="updateApplicationStatus"),
]
