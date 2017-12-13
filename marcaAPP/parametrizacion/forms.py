from django import forms
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm
)
from parametrizacion.models import (User)
# Register your models here.

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User