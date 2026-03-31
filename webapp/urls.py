"""URL routes for the image encryption web app."""

from __future__ import annotations

from django.urls import path

from webapp.views import index_view


urlpatterns = [
    path("", index_view, name="index"),
]
