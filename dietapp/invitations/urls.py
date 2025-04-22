from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_invitation, name='send_invitation'),
]
