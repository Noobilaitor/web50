from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from .models import *
from django.core.files.storage import FileSystemStorage

# Create your views here.

def index(request):
    return render(request, "employment/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "employment/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "employment/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        first = request.POST["first name"]
        last = request.POST["last name"]
        username = request.POST["username"]
        email = request.POST["email"]
        
        image = request.FILES['image']
        fs = FileSystemStorage()
        fs.save(image.name, image)
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "employment/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password,first_name=first,last_name=last, profile_pic=image, employee=True)
            user.save()
        except IntegrityError:
            return render(request, "employment/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "employment/register.html")

def emp_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        image = request.FILES['image']
        fs = FileSystemStorage()
        fs.save(image.name, image)

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "employment/emp_register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, profile_pic=image, employer=True)
            user.save()
        except IntegrityError:
            return render(request, "employment/emp_register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "employment/emp_register.html")

def create_CV(request):
    if request.method == "POST":
        if request.user.employee: 
            user = request.user
            education = request.POST["education"]
            career = request.POST["career"]
            skills = request.POST["skills"]
            about = request.POST["about"]
            new_CV = CV.objects.create(person=user,education=education,career=career,skills=skills,description=about)
            new_CV.save()
            user.has_CV = True
            user.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "employment/create_CV.html", {
                "message": "You are not an employee."
            })
    else:
        return render(request, "employment/create_CV.html")

def allCVs(request):
    CVs = CV.objects.all()
    return render(request, "employment/allCVs.html", {
        "CVs": CVs
    })

def edit_CV(request):
    cv = CV.objects.get(person=request.user)
    if request.method == "POST":
        education = request.POST["education"]
        career = request.POST["career"]
        skills = request.POST["skills"]
        about = request.POST["about"]
        cv.education = education
        cv.skills = skills
        cv.description = about
        cv.career = career
        cv.save() 
        return HttpResponseRedirect(reverse("index"))
    else:     
        cv = CV.objects.get(person=request.user)
        return render(request, "employment/create_CV.html",{
            "edu": cv.education,
            "skills": cv.skills,
            "description": cv.description,
            "career": cv.career,
        })
