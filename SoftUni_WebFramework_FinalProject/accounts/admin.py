
from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from SoftUni_WebFramework_FinalProject.accounts.forms import CustomUserChangeForm, UserCreateForm

UserModel = get_user_model()


@admin.register(UserModel)
class UserAdmin(auth_admin.UserAdmin):
    form = CustomUserChangeForm
    add_form = UserCreateForm

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email", "money")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # list_display = ('username', 'money')
