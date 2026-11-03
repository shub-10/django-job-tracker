from django.http import JsonResponse
from django.contrib.auth import authenticate, login 
from .models import User, JobPost, Application
import json

Allowed_Roles = [User.Role.CANDIDATE, User.Role.RECRUITER]


def health_check(request) -> JsonResponse:
    return JsonResponse({"status": "ok"})

def loginUser(request) -> JsonResponse:
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
        return JsonResponse({"id":user.id,"message":"User logged in successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

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

def getJobPosts(request) ->JsonResponse:
    try:
        jobPosts = JobPost.objects.all().values()
        # print(jobPosts)
        return JsonResponse({"jobPosts": list(jobPosts)}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def createJobPost(request) ->JsonResponse:
    
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"error:":"User is not authenticated"}, status=401)

        if request.user.role != User.Role.RECRUITER:
            return JsonResponse({"error:":"User is not a recruiter"}, status=403)

        data = json.loads(request.body)
        title = data.get("title")
        company = data.get("company")
        experience = data.get("experience")
        description = data.get("description")
        location = data.get("location")

        if not title or not experience or not description or not location:
            return JsonResponse({"error:": "Missing required fields"}, status=400)

        jobPost = JobPost.objects.create(title=title, company=company, experience=experience, description=description, location=location)


        return JsonResponse({"id":jobPost.id,"message":"Job post created successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def getJobPostById(request, jobPostId) ->JsonResponse:
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"error:":"User is not authenticated"}, status=401)

        if request.user.role != User.Role.CANDIDATE:
            return JsonResponse({"error:":"User is not a candidate"}, status=403)

        jobPost = JobPost.objects.get(id=jobPostId)
        if Application.objects.filter(jobPost=jobPost, user=request.user).exists():
            return JsonResponse({"error:":"You have already applied for this job"}, status=400)

        Application.objects.create(jobPost=jobPost, user=request.user)
        return JsonResponse({"message":"Application submitted successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
