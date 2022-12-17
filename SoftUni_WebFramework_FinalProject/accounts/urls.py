from django.urls import path

from SoftUni_WebFramework_FinalProject.accounts.views import SignInView, SignOutView, SignUpView, ProfileDetailView, \
    ProfileEditView, AllProfilePosts

urlpatterns = (
    path('login/', SignInView.as_view(), name='login'),
    path('register/', SignUpView.as_view(), name='register'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile'),
    path('<int:pk>/posts', AllProfilePosts.as_view(), name='posts profile'),
    path('<int:pk>/edit', ProfileEditView.as_view(), name='edit profile'),
)

