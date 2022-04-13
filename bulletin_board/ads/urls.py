from django.urls import path
from .views import *


urlpatterns = [
    path('', AdtList.as_view()),
    path('<int:pk>/', AdtDetailView.as_view(), name='adt_detail'),
    path('adt_create/', AdtCreateView.as_view(), name='adt_create'),
    path('adt_update/<int:pk>/', AdtUpdateView.as_view(), name='adt_update'),
    path('adt_delete/<int:pk>/', AdtDeleteView.as_view(), name='adt_delete'),

    path('user_response/', user_response, name='user_response'),
]