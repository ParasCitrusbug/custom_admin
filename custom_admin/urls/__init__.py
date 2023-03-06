from django.urls import include, path

from . import urls_auth, urls_core,urls_employee

urlpatterns = [
    path("", include(urls_core)),
    path("", include(urls_auth)),
    path("", include(urls_employee))
]
