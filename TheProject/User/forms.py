# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Update this import line

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("email",)


