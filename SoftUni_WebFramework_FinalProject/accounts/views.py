from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth import views as auth_views, get_user_model
from django.urls import reverse_lazy
from django.views import generic as views

from SoftUni_WebFramework_FinalProject.accounts.forms import UserCreateForm

UserModel = get_user_model()


class SignInView(auth_views.LoginView):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super(SignInView, self).dispatch(request, *args, **kwargs)

    template_name = 'accounts/login.html'


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('index')


class SignUpView(views.CreateView):
    template_name = 'accounts/register.html'
    # model = UserModel
    # fields = ('username', 'password',)
    form_class = UserCreateForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')

        return super(SignUpView, self).dispatch(request, *args, **kwargs)


class ProfileDetailView(views.DetailView):
    model = UserModel

    template_name = 'accounts/profile-details.html'
