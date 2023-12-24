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

categories = ["engineer","medicine","business"]

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
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "employment/register.html", {
                "message": "Passwords must match."
            })
        try:
            image = request.FILES['image']
        except MultiValueDictKeyError:
            try:
                user = User.objects.create_user(username, email, password,first_name=first,last_name=last, employee=True)
                user.save()
            except IntegrityError:
                return render(request, "employment/register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        fs = FileSystemStorage()
        fs.save(image.name, image)
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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "employment/emp_register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            image = request.FILES['image']
        except MultiValueDictKeyError:
            try:
                user = User.objects.create_user(username, email, password, employer=True)
                user.save()
            except IntegrityError:
                return render(request, "employment/emp_register.html", {
                    "message": "Username already taken."
                })
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        fs = FileSystemStorage()
        fs.save(image.name, image)
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
            if not request.user.has_CV:       
                user = request.user
                education = request.POST["education"]
                career = request.POST["career"]
                skills = request.POST["skills"]
                about = request.POST["about"]
                job = request.POST["cat"]
                major = request.POST["s_cat"]
                new_CV = CV.objects.create(job=job, major=major, person=user,education=education,career=career,skills=skills,description=about)
                new_CV.save()
                user.has_CV = True
                user.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "employment/create_CV.html", {
                "message": "You already have a CV.",
                "cats": categories
            })
        else:
            return render(request, "employment/create_CV.html", {
                "message": "You are not an employee.",
                "cats": categories
            })
    else:
        return render(request, "employment/create_CV.html",{
            "cats": categories
        })

def allCVs(request):
    CVs = CV.objects.all().order_by("-id")
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
        job = request.POST["cat"]
        major = request.POST["s_cat"]
        cv.education = education
        cv.skills = skills
        cv.description = about
        cv.career = career
        cv.job = job
        cv.major = major
        cv.save() 
        return HttpResponseRedirect(reverse("index"))
    else:     
        cv = CV.objects.get(person=request.user)
        return render(request, "employment/create_CV.html",{
            "edu": cv.education,
            "skills": cv.skills,
            "description": cv.description,
            "career": cv.career,
            "cats":categories,
            "job": cv.job,
            "major": cv.major,
        })

def filter_CV(request):
    return render(request, "employment/filter_CV.html",{
            "cats": categories
        })

def search(request, content):
    content = content.split(",")
    Cvs = CV.objects.all()
    name = []
    desc = []
    skilll = []
    job = []
    for cv in Cvs:
        chosen_type = "c"
        chosen_job = "m"
        chosen_skill = "n"
        if content[0] != "":
            all_skills = cv.skills
            all_skills = all_skills.split(",")
            skills = []
            for skill in all_skills:
                skill = skill.replace(" ", "")
                skills.append(skill)
            if content[0] in skills:
                chosen_skill = cv
        else:
            chosen_skill = cv
        if cv.job == content[1] or content[1] == "":
            chosen_job = cv
        if cv.major == content[2] or content[2] == "---" or content[2] == "":
            chosen_type = cv
        if chosen_type == chosen_job == chosen_skill:
            name.append(cv.person.username)
            desc.append(cv.description)
            skilll.append(cv.skills)
            job.append(cv.job)
    return JsonResponse({"name": name, "desc": desc, "job": job, "skill": skilll,})
    
def profile(request, user):
    user = User.objects.get(username=user)
    cv = CV.objects.get(person=user)
    return render(request, "employment/profile.html", {
        "cv": cv
    })
