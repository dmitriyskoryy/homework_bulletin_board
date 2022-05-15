from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *

urlpatterns = [
    path('first_login/', FirstLoginView.as_view()),
    path('register_code/', register_code),
]