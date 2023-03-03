from django.urls import include, path

from . import urls_auth, urls_core

urlpatterns = [
    path("", include(urls_core)),
    path("", include(urls_auth)),
]
