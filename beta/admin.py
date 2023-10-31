from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, PasswordToken
from .forms import NewUserForm, NewUserChangeForm
from django.contrib.auth.admin import UserAdmin  as BaseUserAdmin
from django.contrib.auth.models import Group

class NewUserAdmin(BaseUserAdmin):
    add_form     = NewUserChangeForm
    form         = NewUserForm
    model        = User
    list_display = ("username", "email", "sub_id", "status", "is_staff", "is_active",)
    list_filter   = ("username", "email", "is_staff", "is_active",)
    fieldsets     = (
        (None, {"fields": ("username", "email", "sub_id", "status", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("username", "email")
    ordering     = ("username", "email")

admin.site.register(User, NewUserAdmin)
admin.site.register(PasswordToken)