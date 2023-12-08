
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_post", views.create_post, name="create_post"),
    path("users/<str:profile>", views.profile, name="profile"),
    path("users/<str:profile>/follow", views.follow, name="follow"),
    path("users/<str:profile>/unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    
    #API routes
    path("edit/<int:post_id>", views.edit, name="edit"),
]
