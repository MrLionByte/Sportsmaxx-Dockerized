from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_banner, name="show_banner"),
    path("add/", views.add_banner, name="add_banner"),
    path("edit/", views.edit_banner, name="edit_banner"),
    path("list/", views.list_banner, name="list_banner"),
    path("unlist/", views.unlist_banner, name="unlist_banner"),
]
