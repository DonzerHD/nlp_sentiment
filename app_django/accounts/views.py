from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView , LoginView
from django.views.generic import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from .models import Patient

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    success_url = '/'

    def get_success_url(self):
        return self.success_url
    
class CustomLogoutView(LogoutView):
    next_page = 'login'

