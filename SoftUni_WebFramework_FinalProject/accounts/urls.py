from django.urls import path

from SoftUni_WebFramework_FinalProject.accounts.views import SignInView, SignOutView, SignUpView, ProfileDetailView

urlpatterns = (
    path('login/', SignInView.as_view(), name='login'),
    path('register/', SignUpView.as_view(), name='register'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile'),
)

