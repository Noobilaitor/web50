from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from .models import *

def index(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            contents = request.POST["contents"]
            user = request.user
            post = Posts.objects.create(creator=user, contents=contents)
            post.save()
            return render(request, "network/index.html", {
                "posts": Posts.objects.all()
            })
        else:
            return render(request, "network/login.html")
    else:
        return render(request, "network/index.html", {
                "posts": Posts.objects.all()
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def create_post(request):
    return render(request, "network/create_post.html")

def follow(request, profile):
    if request.user.is_authenticated:
        cur_profile = User.objects.get(username=profile)
        try:
            follow_user = Followers.objects.create(following=cur_profile, followers=request.user)
            follow_user.save()
            
        except IntegrityError:
            user_posts = Posts.objects.filter(creator=cur_profile.id).all()
            follow_num = cur_profile.following.all()
            following_num = cur_profile.followers.all()
            return render(request, "network/profile.html", {
                "profile": profile,
                "cur_profile": cur_profile,
                "user_posts": user_posts,
                "follow_num": follow_num.count(),
                "following_num": following_num.count(),
                "message": 'You already follow this user'
            })
        user_posts = Posts.objects.filter(creator=cur_profile.id).all()
        follow_num = cur_profile.following.all()
        following_num = cur_profile.followers.all()
        return render(request, "network/profile.html", {
            "profile": profile,
            "cur_profile": cur_profile,
            "user_posts": user_posts,
            "follow_num": follow_num.count(),
            "following_num": following_num.count(),
        })
    else:
        return HttpResponseRedirect(reverse("register"))

def profile(request, profile):
    cur_profile = User.objects.get(username=profile)
    user_posts = Posts.objects.filter(creator=cur_profile.id).all()
    follow_num = cur_profile.following.all()
    following_num = cur_profile.followers.all()
    try:
        follow_user = Followers.objects.get(following=cur_profile, followers=request.user)
    except (TypeError,ObjectDoesNotExist):
        return render(request, "network/profile.html", {
        "profile": profile,
        "cur_profile": cur_profile,
        "user_posts": user_posts,
        "follow_num": follow_num.count(),
        "following_num": following_num.count(),
        "btn": "follow",
    })
    return render(request, "network/profile.html", {
        "profile": profile,
        "cur_profile": cur_profile,
        "user_posts": user_posts,
        "follow_num": follow_num.count(),
        "following_num": following_num.count(),
    })

def unfollow(request, profile):
    if request.user.is_authenticated:
        cur_profile = User.objects.get(username=profile)
        try:
            follow_user = Followers.objects.get(following=cur_profile, followers=request.user)
            follow_user.delete()
        except ObjectDoesNotExist:
            user_posts = Posts.objects.filter(creator=cur_profile.id).all()
            follow_num = cur_profile.following.all()
            following_num = cur_profile.followers.all()
            return render(request, "network/profile.html", {
                "profile": profile,
                "cur_profile": cur_profile,
                "user_posts": user_posts,
                "follow_num": follow_num.count(),
                "following_num": following_num.count(),
                "message": 'You do not follow this user'
            })
        user_posts = Posts.objects.filter(creator=cur_profile.id).all()
        follow_num = cur_profile.following.all()
        following_num = cur_profile.followers.all()
        return render(request, "network/profile.html", {
            "profile": profile,
            "cur_profile": cur_profile,
            "user_posts": user_posts,
            "follow_num": follow_num.count(),
            "following_num": following_num.count(),
            "btn": "follow",
        })
    else:
        return HttpResponseRedirect(reverse("register"))
