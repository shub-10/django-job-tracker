from typing import Any
from django.http import JsonResponse
from django.contrib.auth import authenticate, login 
from .models import User, JobPost, Application
import json
from django.views.decorators.http import require_GET, require_POST
from django.db import IntegrityError
Allowed_Roles = [User.Role.CANDIDATE, User.Role.RECRUITER]


def health_check(request) -> JsonResponse:
    return JsonResponse({"status": "ok"})

def check_role(request, role) -> JsonResponse:
    if request.user.role != role:
        return JsonResponse({"error:":"User is not a " + role}, status=403)
    return JsonResponse({"message":"User is a " + role}, status=200)

@require_POST
def signup(request) -> JsonResponse:
    try:
        data = json.loads(request.body)

        email = data.get("email")
        password = data.get("password")
        role = data.get("role")
        
        if not email or not password or not role:
            return JsonResponse({"error:": "Missing required fields"}, status=400)
        if role not in Allowed_Roles:
            return JsonResponse({"error:": "Invalid role"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error:": "Email already exists"}, status=400)

        user = User.objects.create_user(username=email,email=email, password=password, role=role)
        return JsonResponse({"id":user.id,"message":"User created successfully"}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except KeyError:
        return JsonResponse({"error": "Missing required fields"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def login_user(request) -> JsonResponse:
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return JsonResponse({"error:": "Missing required fields"}, status=400)
        user = authenticate(request, email=email, password=password)
        # print("user is", user.id, user.email, user.role)
        
        if user is None:
            return JsonResponse({"error:": "Invalid credentials"}, status=400)
        login(request, user)
        return JsonResponse({"id":user.id, "role":user.role, "message":"User logged in successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@require_GET
def get_job_posts(request) -> JsonResponse:
    try:
        jobPosts = JobPost.objects.all().values()
        # print(jobPosts)
        return JsonResponse({"jobPosts": list(jobPosts)}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_POST
def create_job_post(request) -> JsonResponse:
    
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"error:":"User is not authenticated"}, status=401)
        response = check_role(request, User.Role.RECRUITER)
        if response.status_code == 403:
            return response
        # if request.user.role != User.Role.RECRUITER:  
        #     return JsonResponse({"error:":"User is not a recruiter"}, status=403)

        data = json.loads(request.body)
        title = data.get("title")
        company = data.get("company")
        experience = data.get("experience")
        description = data.get("description")
        location = data.get("location")
        postedBy = request.user

        if not title or not experience or not description or not location:
            return JsonResponse({"error:": "Missing required fields"}, status=400)

        jobPost = JobPost.objects.create(title=title, company=company, experience=experience, description=description, location=location, postedBy=postedBy)


        return JsonResponse({"id":jobPost.id,"message":"Job post created successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_POST
def apply_for_job(request, job_post_id) -> JsonResponse:

    try:
        if not request.user.is_authenticated:
            return JsonResponse({"error:":"User is not authenticated"}, status=401)

        response = check_role(request, User.Role.CANDIDATE)
        if response.status_code == 403:
            return response
        # if request.user.role != User.Role.CANDIDATE:
        #     return JsonResponse({"error:":"User is not a candidate"}, status=403)
        jobPost = JobPost.objects.get(id=job_post_id)

        if jobPost is None:
            return JsonResponse({"error:":"Job post not found"}, status=404)
        if Application.objects.filter(jobPost=jobPost, user=request.user).exists():
            return JsonResponse({"error:":"You have already applied for this job"}, status=400)

        phone = request.POST.get("phone")
        resume = request.FILES.get("resume")
        if not resume:
            return JsonResponse({"error:":"Resume is required"}, status=400)
        if resume.content_type != "application/pdf" or not resume.name.endswith(".pdf"):
            return JsonResponse({"error:":"Resume must be a PDF"}, status=400)
        if resume.size > 10 * 1024 * 1024:
            return JsonResponse({"error:":"Resume is too large"}, status=400)
        if not phone:
            return JsonResponse({"error:":"Phone is required"}, status=400)
        if not phone.isdigit():
            return JsonResponse({"error:":"Phone is not a number"}, status=400)
        if len(phone) != 10:
            return JsonResponse({"error:":"Phone is not a valid number"}, status=400)

        Application.objects.create(jobPost=jobPost, user=request.user, phone=phone, resume=resume)
        return JsonResponse({"message":"Application submitted successfully"}, status=201)
    except IntegrityError:
        return JsonResponse({"error:":"You have already applied for this job"}, status=409)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_GET
def get_my_applications(request) -> JsonResponse:
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"error:": "User is not authenticated"}, status=401)
        response = check_role(request, User.Role.CANDIDATE)
        if response.status_code == 403:
            return response
        # if request.user.role == User.Role.RECRUITER:
        #     return JsonResponse({"error:": "User is not a candidate"}, status=403)
        userApplications = Application.objects.filter(user=request.user).values()

        # jobs = JobPost.objects.filter(id__in=jobIds).values()
        # That is “job posts that have an application by this user.”
        # userApplications = JobPost.objects.filter(application__user=request.user).distinct().values()

        return JsonResponse({"user applications": list[Any](userApplications)}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_GET
def get_job_posts_by_me(request) -> JsonResponse:

    try:
        if not request.user.is_authenticated:
            return JsonResponse({"error:": "User is not authenticated"}, status=401)
        if request.user.role != User.Role.RECRUITER:
            return JsonResponse({"error:": "User is not a recruiter"}, status=403)
        jobs = JobPost.objects.filter(postedBy=request.user).values()
        return JsonResponse({"jobs": list[Any](jobs)}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@require_GET
def get_applications_for_job_post(request, job_post_id) -> JsonResponse:
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"error:": "User is not authenticated"}, status=401)
        response = check_role(request, User.Role.RECRUITER)
        if response.status_code == 403:
            return response
        # if request.user.role != User.Role.RECRUITER:
        #     return JsonResponse({"error:": "User is not a recruiter"}, status=403)
        jobPost = JobPost.objects.get(id=job_post_id)
        if jobPost.postedBy != request.user:
            return JsonResponse({"error:": "User is not the recruiter of the job post"}, status=403)
        applications = Application.objects.filter(jobPost=job_post_id).values()

        return JsonResponse({"applications": list[Any](applications)}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)})


@require_POST
def update_application_status(request, application_id) -> JsonResponse:
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"error:": "User is not authenticated"}, status=401)

        response = check_role(request, User.Role.RECRUITER)
        if response.status_code == 403:
            return response
        #if request.user.role != User.Role.RECRUITER:
        #     return JsonResponse({"error:": "User is not a recruiter"}, status=403)

        application = Application.objects.get(id=application_id)

        data = json.loads(request.body)
        currentStatus = data.get("currentStatus")
        if currentStatus != application.status:
            application.status = currentStatus
            application.save()
            return JsonResponse({"message": "Application status updated successfully"}, status=200)
        else:
            return JsonResponse({"message": "Application status is already updated"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)})
        

        