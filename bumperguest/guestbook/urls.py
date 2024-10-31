from django.urls import path

from . import views

urlpatterns = [
    path("entry", views.EntryView, name="entry"),
    path("user/data", views.get_user_data, name="get-user-data"),
]
