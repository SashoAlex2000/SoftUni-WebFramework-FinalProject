from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth import views as auth_views, get_user_model
from django.urls import reverse_lazy
from django.views import generic as views

from SoftUni_WebFramework_FinalProject.accounts.forms import UserCreateForm
from SoftUni_WebFramework_FinalProject.mlo_store.models import Item

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


class ProfileEditView(views.UpdateView):
    class Meta:
        model = UserModel
        fields = ("username", "first_name", "last_name", "gender")
        help_texts = {
            'username': None,
            'email': None,
        }

    model = UserModel

    template_name = 'accounts/profile-edit.html'
    fields = ('username', 'first_name', 'last_name', 'gender')


class ProfileDeleteView(views.DeleteView):
    template_name = 'accounts/profile-delete-page.html'
    model = UserModel
    success_url = reverse_lazy('index')


class AllProfilePosts(views.ListView):
    model = Item

    template_name = 'accounts/all-posts-by-profile.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        print(queryset)
        queryset.filter(owner_id=self.request.user)
        current_pk = self.kwargs['pk']
        new_query_set_list = []
        for item in queryset:
            print(item.owner_id)
            print(current_pk)
            if item.owner_id == current_pk:
                new_query_set_list.append(item)
        print(new_query_set_list)
        return new_query_set_list
