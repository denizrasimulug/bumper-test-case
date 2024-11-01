from django.urls import path

from . import views

urlpatterns = [
    path("entry", views.EntryView.as_view(), name="entry-view"),
    path("user/data", views.get_user_data, name="user-data-view"),
]
