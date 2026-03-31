"""Application configuration for the web interface."""

from __future__ import annotations

from django.apps import AppConfig


class WebappConfig(AppConfig):
    """Configuration for the image encryption web app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "webapp"
