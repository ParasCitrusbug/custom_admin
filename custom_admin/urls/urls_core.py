"""
A request in Django first comes to urls.py and then goes to the matching function in views.py.
Python functions in views.py take the web request from urls.py and give the web response to templates
"""

from django.urls import path

from custom_admin import views

app_name = "user"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # User Module
    path("users/", views.UserListView.as_view(), name="user-list"),
    path("users/create/", views.UserCreateView.as_view(), name="user-create"),
    path("users/<uuid:pk>/update/", views.UserUpdateView.as_view(), name="user-update"),
    path(
        "users/<uuid:pk>/password/",
        views.UserPasswordView.as_view(),
        name="user-password",
    ),
    path("users/<uuid:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
    path("users/<uuid:pk>", views.UserDetailView.as_view(), name="user-detail"),
    path("users-ajax/", views.UserListAjaxView.as_view(), name="user-list-ajax"),
]
