from django.urls import path
from . import views

app_name = 'invitations'

urlpatterns = [
    path('create/', views.create_invitation, name='create_invitation'),
    path('<uuid:token>/resend/', views.resend_invitation, name='resend_invitation'),
    path('<uuid:token>/', views.invite_register, name='invite_register'),
]
