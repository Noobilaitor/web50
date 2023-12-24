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
    path("edit", views.edit_CV, name="edit_CV"),
    path("filter/CVs", views.filter_CV, name="filter_CV"),
    
    #API routes
    path("filter/search/<str:content>", views.search, name="filter_CV")
]