from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class NewUserForm(UserCreationForm):

    class Meta:
        model  = User
        fields = ["username", "email",]

class NewUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model  = User
        fields = ["username", "email",]