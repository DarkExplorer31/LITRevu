from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=25, label="Nom d'utilisateur")
    password = forms.CharField(
        max_length=50, widget=forms.PasswordInput, label="Mot de Passe"
    )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]
