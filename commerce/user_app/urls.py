from django.contrib.auth import views as auth_views
from django.urls import path
from allauth.account.forms import SignupForm
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('signin/', views.SignUp, name='signup'),
  
]