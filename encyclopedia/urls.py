from django.urls import path

from . import views

urlpatterns = [
    path("NewPage", views.NewPage, name="NewPage"),
    path("search", views.search, name="search"),
    path("", views.index, name="index"),
    path("<str:title>", views.EntryPage, name="EntryPage")
]
