from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("register/employer", views.emp_register, name="emp_register"),
    path("create_CV", views.create_CV, name="create_CV"),
    path("allCVs", views.allCVs, name="allCVs"),
    path("edit/CV", views.edit_CV, name="edit_CV"),
    path("filter/CVs", views.filter_CV, name="filter_CV"),
    path("filter/CVs/<str:type>", views.filter_CVV, name="filter_CVV"),
    path("user/<str:user>", views.profile, name="profile"),
    path("create_job", views.create_job, name="create_job"),
    path("alljobs", views.alljobs, name="alljobs"),
    path("edit/job", views.edit_job, name="edit_job"),
    path("filter/jobs", views.filter_job, name="filter_job"),
    path("filter/jobs/<str:type>", views.filter_jobb, name="filter_jobb"),
    
    #API routes
    path("filter/search/<str:content>", views.search, name="filter_CV"),
    path("filter/search_job/<str:content>", views.search_job, name="filter_job")
]
