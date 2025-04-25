from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_invitation, name='send_invitation'),
    path('register/<uuid:token>/', views.register_with_token, name='register_with_token'),
]
