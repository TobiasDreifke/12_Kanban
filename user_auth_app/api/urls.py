
from django.urls import path

from user_auth_app.api.views import RegistrationView, LoginView, LogoutView

urlpatterns = [
    path('api/registration/', RegistrationView.as_view(), name='registration'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
]