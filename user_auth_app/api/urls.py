"""URL routes for user authentication API.

Defines registration, login and logout endpoints and is intended to be
included under the project's `api/` prefix.
"""

from django.urls import path

from user_auth_app.api.views import RegistrationView, LoginView, LogoutView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]