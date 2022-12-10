from django.shortcuts import render

# Create your views here.

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import generic as views

from SoftUni_WebFramework_FinalProject.accounts.forms import UserCreateForm


class SignInView(auth_views.LoginView):
    template_name = 'accounts/login.html'


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')


class SignUpView(views.CreateView):
    template_name = 'accounts/register.html'
    # model = UserModel
    # fields = ('username', 'password',)
    form_class = UserCreateForm
    success_url = reverse_lazy('index')
