"""App configuration for the kanban application.

Declares the application config class used by Django to load the
`kanban_app` application and its configuration.
"""

from django.apps import AppConfig


class KanbanAppConfig(AppConfig):
    """Django AppConfig for the kanban application."""
    name = "kanban_app"
