from django.urls import path
from . import views

app_name = 'invitations'

urlpatterns = [
    path('send/', views.send_invitation, name='send_invitation'),
    path('<uuid:token>/', views.invite_register, name='invite_register'),
]
