from django.urls import path

from .views import *

urlpatterns = [
    path('first_login/', FirstLoginView.as_view()),
    path('register_code/', register_code),
]