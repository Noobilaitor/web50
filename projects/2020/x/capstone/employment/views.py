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
    CVs = CV.objects.filter(is_active=True).all()
    jobs = Job.objects.filter(is_active=True).all()
    return render(request, "employment/index.html",{
        "cats": categories,
        "CVs": CVs,
        "jobs": jobs,
    })

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
    if request.user.is_authenticated:
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
    else:
        return HttpResponseRedirect(reverse("register"))

def allCVs(request):
    CVs = CV.objects.filter(is_active=True).all().order_by("-id")
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
            "cats": categories,
        })

def filter_CVV(request, type):
    return render(request, "employment/filter_CV.html",{
            "cats": categories,
            "type": type
        })

def search(request, content):
    content = content.split(",")
    Cvs = CV.objects.filter(is_active=True).all()
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
    try:
        cv = CV.objects.get(person=user)
    except:
        job = Job.objects.get(person=user)
        return render(request, "employment/com_profile.html", {
            "job": job
        })
    
    return render(request, "employment/profile.html", {
        "cv": cv,
    })

def create_job(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.employer:     
                user = request.user
                salary = request.POST["salary"]
                skills = request.POST["skills"]
                desc = request.POST["desc"]
                job = request.POST["cat"]
                major = request.POST["s_cat"]
                new_job = Job.objects.create(job=job, major=major, person=user,skills=skills,description=desc, salary=salary)
                new_job.save()
                user.has_job = True
                user.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "employment/create_job.html", {
                    "message": "You are not an employer.",
                    "cats": categories
                })
        else:
            return render(request, "employment/create_job.html",{
                "cats": categories
            })
    else:
        return HttpResponseRedirect(reverse("register"))

def alljobs(request):
    jobs = Job.objects.filter(is_active=True).all().order_by("-id")
    return render(request, "employment/alljobs.html", {
        "jobs": jobs
    })

def edit_job(request):
    job = Job.objects.get(person=request.user)
    if request.method == "POST":
        salary = request.POST["salary"]
        skills = request.POST["skills"]
        desc = request.POST["desc"]
        jobb = request.POST["cat"]
        major = request.POST["s_cat"]
        job.salary = str(salary)
        job.skills = skills
        job.description = desc
        job.job = jobb
        job.major = major
        job.save() 
        return HttpResponseRedirect(reverse("index"))
    else:     
        job = Job.objects.get(person=request.user)
        return render(request, "employment/create_job.html",{
            "salary": job.salary,
            "skills": job.skills,
            "description": job.description,
            "cats":categories,
            "job": job.job,
            "major": job.major,
        })

def filter_job(request):
    return render(request, "employment/filter_job.html",{
            "cats": categories,
        })

def filter_jobb(request, type):
    return render(request, "employment/filter_job.html",{
            "cats": categories,
            "type": type
        })

def search_job(request, content):
    content = content.split(",")
    Jobs = Job.objects.filter(is_active=True).all()
    name = []
    desc = []
    skilll = []
    jobb = []
    for job in Jobs:
        chosen_type = "c"
        chosen_job = "m"
        chosen_skill = "n"
        if content[0] != "":
            all_skills = job.skills
            all_skills = all_skills.split(",")
            skills = []
            for skill in all_skills:
                skill = skill.replace(" ", "")
                skills.append(skill)
            if content[0] in skills:
                chosen_skill = job
        else:
            chosen_skill = job
        if job.job == content[1] or content[1] == "":
            chosen_job = job
        if job.major == content[2] or content[2] == "---" or content[2] == "":
            chosen_type = job
        if chosen_type == chosen_job == chosen_skill:
            name.append(job.person.username)
            desc.append(job.description)
            skilll.append(job.skills)
            jobb.append(job.job)
    return JsonResponse({"name": name, "desc": desc, "job": jobb, "skill": skilll,})

def recruit(request, user):
    cur_user = request.user
    user = User.objects.get(username=user)
    if user.employee and cur_user.employer:
        if cur_user in user.CV_requests.all():
            user.CV_requests.remove(cur_user)
            user.save()
            return JsonResponse({"message": "fail"})
        else:
            user.CV_requests.add(cur_user)
            user.save()
            return JsonResponse({"message": "success"})
    elif user.employer and cur_user.employee:
        if cur_user in user.job_requests.all():
            user.job_requests.remove(cur_user)
            user.save()
            return JsonResponse({"result": "fail"})
        else:
            user.job_requests.add(cur_user)
            user.save()
            return JsonResponse({"result": "success"})

def notification(request):
    return render(request, "employment/notification.html",{
    })

def accept(request, user):
    cur_user = request.user
    user = User.objects.get(username=user)
    if cur_user.employee:
        cv = CV.objects.get(person=cur_user)
        job = Job.objects.get(person=user)
        cv.is_active = False
        job.is_active = False
        cv.save()
        job.save()
        cur_user.working.add(user)
        cur_user.CV_requests.remove(user)
        return JsonResponse({"message": "accepted"})
    elif cur_user.employer:
        cv = CV.objects.get(person=user)
        job = Job.objects.get(person=cur_user)
        cv.is_active = False
        job.is_active = False
        cv.save()
        job.save()
        cur_user.working.add(user)
        cur_user.job_requests.remove(user)
        return JsonResponse({"message": "j_accepted"})
