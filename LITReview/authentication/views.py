from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import View
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from . import forms


class LoginPageView(View):
    template_name = "authentication/login.html"
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = ""
        if request.user.is_authenticated:
            return redirect("home")
        return render(
            request,
            self.template_name,
            context={"form": form, "message": message},
        )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("home")
        message = "Vos identifiants sont invalides"
        return render(
            request,
            self.template_name,
            context={"form": form, "message": message},
        )


class SignupPageView(View):
    template_name = "authentication/signup.html"
    form_class = forms.SignupForm

    def get(self, request):
        form = self.form_class()
        message = ""
        return render(
            request,
            self.template_name,
            context={"form": form, "message": message},
        )

    def post(self, request):
        form = self.form_class(request.POST)
        message = ""
        if form.is_valid():
            user = form.save()
            login(request, user)
            message = f"{user.username}, Vous êtes inscrit"
            return redirect("home")
        return render(
            request,
            self.template_name,
            context={"form": form, "message": message},
        )


class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("home")
    template_name = "authentication/password_change.html"
