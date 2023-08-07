from django.urls import path

from . import views

urlpatterns = [
    path("random", views.randomPage, name="randomPage"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("wiki/<str:title>", views.EntryPage, name="EntryPage"),
    path("NewPage", views.NewPage, name="NewPage"),
    path("search", views.search, name="search"),
    path("", views.index, name="index")
]
