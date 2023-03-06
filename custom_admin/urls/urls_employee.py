"""
A request in Django first comes to urls.py and then goes to the matching function in views.py.
Python functions in views.py take the web request from urls.py and give the web response to templates
"""

from django.urls import path

from custom_admin.views import employees

app_name = "employee"

urlpatterns = [
    path("employees/", employees.EmployeeListView.as_view(), name="employee-list"),
    path(
        "employees/create/",
        employees.EmployeeCreateView.as_view(),
        name="employee-create",
    ),
    path(
        "employees/<uuid:pk>/update/",
        employees.EmployeeUpdateView.as_view(),
        name="employee-update",
    ),
    path(
        "employees/<uuid:pk>/delete/",
        employees.EmployeeDeleteView.as_view(),
        name="employee-delete",
    ),
    path(
        "employees/<uuid:pk>",
        employees.EmployeeDetailView.as_view(),
        name="employee-detail",
    ),
    path(
        "employees-ajax/",
        employees.EmployeeListAjaxView.as_view(),
        name="employee-list-ajax",
    ),
]
