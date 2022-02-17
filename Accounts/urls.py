from django.urls import path
from . import views

urlpatterns = [
    path('Login', views.Login, name='Login'),
    path('Logout', views.Logout, name='Logout'),
    path('Register', views.Register, name='Register'),
    path('UserProfile', views.UserProfile, name='UserProfile'),
    # path('DashboardSubmission', views.DashboardSubmission, name='DashboardSubmission')
]