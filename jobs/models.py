from django.db import models
from django.contrib.auth.models import AbstractUser

class JobPost(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    experience = models.IntegerField()
    description = models.TextField()
    location = models.CharField(max_length=200)


    def __str__(self) -> str:
        return f"{self.title} at {self.company}"

class User(AbstractUser):
  class Role(models.TextChoices):
    CANDIDATE = "candidate", "Candidate"
    RECRUITER = "recruiter", "Recruiter"

  email = models.EmailField(unique=True)
  role = models.CharField(max_length=20 , choices=Role.choices)

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ["username"]



class Application(models.Model):
  class Status(models.TextChoices):
    PENDING = "pending", "Pending"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
    HIRED = "hired", "Hired"
    

  jobPost = models.ForeignKey(JobPost, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
  phone = models.CharField(max_length=15)
  resume = models.FileField(upload_to="resumes/")
  createdAt = models.DateTimeField(auto_now_add=True)
  






  

