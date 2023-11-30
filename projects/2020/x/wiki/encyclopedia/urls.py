from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entries, name="entries"),
    path("error", views.entries, name="error"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("wiki", views.savePage, name="savePage"),
    path("random", views.randomPage, name="randomPage"),
    path("edit", views.edit, name="edit"),
    path("hello", views.saveChanges, name="saveChanges")
]
