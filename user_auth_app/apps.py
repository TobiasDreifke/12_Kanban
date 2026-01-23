"""App configuration for user_auth_app.

Defines the Django application config for authentication related code
such as registration, login and token management.
"""

from django.apps import AppConfig


class UserAuthAppConfig(AppConfig):
    """Django AppConfig for the user authentication application."""
    name = "user_auth_app"
