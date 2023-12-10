from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from .models import *

def index(request):
    posts = Posts.objects.all().order_by('-id')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    likes = Likes.objects.all()
    liked_posts = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                liked_posts.append(like.post.id)
    except:
        liked_posts = []
    if request.method == "POST":
        if request.user.is_authenticated:
            contents = request.POST["contents"]
            user = request.user
            post = Posts.objects.create(creator=user, contents=contents)
            post.save()
            return render(request, "network/index.html", {
                "posts": posts,
                "page_obj": page_obj,
                "title": 'All Posts',
                "liked_posts": liked_posts,
            })
        else:
            return render(request, "network/login.html")
    else:
        return render(request, "network/index.html", {
                "posts": posts,
                "page_obj": page_obj,
                "title": 'All Posts',
                "liked_posts": liked_posts,
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
    return HttpResponseRedirect(reverse("login"))

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

@login_required
def follow(request, profile):
    likes = Likes.objects.all()
    liked_posts = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                liked_posts.append(like.post.id)
    except:
        liked_posts = []
    if request.user.is_authenticated:
        cur_profile = User.objects.get(username=profile)
        try:
            follow_user = Followers.objects.create(following=cur_profile, followers=request.user)
            follow_user.save()
            
        except IntegrityError:
            user_posts = Posts.objects.filter(creator=cur_profile.id).all().order_by('-id')
            follow_num = cur_profile.following.all()
            following_num = cur_profile.followers.all()
            paginator = Paginator(user_posts, 10
    )
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(request, "network/profile.html", {
                "profile": profile,
                "cur_profile": cur_profile,
                "posts": user_posts,
                "follow_num": follow_num.count(),
                "following_num": following_num.count(),
                "page_obj": page_obj,
                "title": f"{cur_profile.username}'s Posts",
                "liked_posts": liked_posts,
                "message": 'You already follow this user'
            })
        user_posts = Posts.objects.filter(creator=cur_profile.id).all().order_by('-id')
        follow_num = cur_profile.following.all()
        following_num = cur_profile.followers.all()
        paginator = Paginator(user_posts, 10
)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/profile.html", {
            "profile": profile,
            "cur_profile": cur_profile,
            "posts": user_posts,
            "follow_num": follow_num.count(),
            "page_obj": page_obj,
            "title": f"{cur_profile.username}'s Posts",
            "liked_posts": liked_posts,
            "following_num": following_num.count(),
        })
    else:
        return HttpResponseRedirect(reverse("register"))

def profile(request, profile):
    likes = Likes.objects.all()
    liked_posts = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                liked_posts.append(like.post.id)
    except:
        liked_posts = []
    cur_profile = User.objects.get(username=profile)
    user_posts = Posts.objects.filter(creator=cur_profile.id).all().order_by('-id')
    follow_num = cur_profile.following.all().order_by('id')
    following_num = cur_profile.followers.all().order_by('id')
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        follow_user = Followers.objects.get(following=cur_profile, followers=request.user)
    except (TypeError,ObjectDoesNotExist):
        return render(request, "network/profile.html", {
        "profile": profile,
        "cur_profile": cur_profile,
        "posts": user_posts,
        "follow_num": follow_num.count(),
        "following_num": following_num.count(),
        "btn": "follow",
        "title": f"{cur_profile.username}'s Posts",
        "liked_posts": liked_posts,
        "page_obj": page_obj
    })
    return render(request, "network/profile.html", {
        "profile": profile,
        "cur_profile": cur_profile,
        "posts": user_posts,
        "follow_num": follow_num.count(),
        "following_num": following_num.count(),
        "title": f"{cur_profile.username}'s Posts",
        "liked_posts": liked_posts,
        "page_obj": page_obj
    })

@login_required
def unfollow(request, profile):
    likes = Likes.objects.all()
    liked_posts = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                liked_posts.append(like.post.id)
    except:
        liked_posts = []
    if request.user.is_authenticated:
        cur_profile = User.objects.get(username=profile)
        try:
            follow_user = Followers.objects.get(following=cur_profile, followers=request.user)
            follow_user.delete()
        except ObjectDoesNotExist:
            user_posts = Posts.objects.filter(creator=cur_profile.id).all().order_by('-id')
            follow_num = cur_profile.following.all()
            following_num = cur_profile.followers.all()
            paginator = Paginator(user_posts, 10
    )
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(request, "network/profile.html", {
                "profile": profile,
                "cur_profile": cur_profile,
                "posts": user_posts,
                "follow_num": follow_num.count(),
                "following_num": following_num.count(),
                "message": 'You do not follow this user',
                "title": f"{cur_profile.username}'s Posts",
                "liked_posts": liked_posts,
                "page_obj": page_obj
            })
        user_posts = Posts.objects.filter(creator=cur_profile.id).all().order_by('-id')
        follow_num = cur_profile.following.all()
        following_num = cur_profile.followers.all()
        paginator = Paginator(user_posts, 10
)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/profile.html", {
            "profile": profile,
            "cur_profile": cur_profile,
            "posts": user_posts,
            "follow_num": follow_num.count(),
            "following_num": following_num.count(),
            "btn": "follow",
            "title": f"{cur_profile.username}'s Posts",
            "liked_posts": liked_posts,
            "page_obj": page_obj
        })
    else:
        return HttpResponseRedirect(reverse("register"))

@login_required
def following(request):
    likes = Likes.objects.all()
    liked_posts = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                liked_posts.append(like.post.id)
    except:
        liked_posts = []
    user = request.user
    if user.is_authenticated:
        user_following = Followers.objects.filter(followers=user).all()
        all_followers = []
        follow_posts = []
        for followerr in user_following:
            followerr = User.objects.get(username=followerr.following)
            all_followers.append(followerr)
            
        for follower in all_followers:
            follow_post = Posts.objects.filter(creator=follower).all()
            for post in follow_post:
                follow_posts.append(post)
                print(follow_post)
        if follow_posts == []:
            return render(request, "network/following.html", )
        else:  
            follow_posts.reverse()
            paginator = Paginator(follow_posts, 10
    )
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            return render(request, "network/following.html", {
                "title": 'Following',
                "posts": follow_post,
                "page_obj": page_obj,
                "liked_posts": liked_posts
            })
    else:
        return HttpResponseRedirect(reverse("register"))

@login_required
def edit(request, post_id):
    post = Posts.objects.get(pk=post_id)
    creator = post.creator
    if request.user == creator:
        if request.method == 'POST':
            data = json.loads(request.body)
            post.contents = data["content"]
            post.save()
            return JsonResponse({"data": data["content"]})
    else:
        return HttpResponseRedirect(reverse(index))

@login_required
def like(request, post_id):
    user = request.user
    user = User.objects.get(pk=user.id)
    post = Posts.objects.get(pk=post_id)
    try:
        like = Likes.objects.get(user=user,post=post)
    except:
        add_like = Likes(user=user,post=post)
        add_like.save()
        like_num = post.liked_post.count()
        return JsonResponse({"message": "liked", "like_num": like_num})
    like.delete()
    like_num = post.liked_post.count()
    return JsonResponse({"message": "Unliked", "like_num": like_num})
