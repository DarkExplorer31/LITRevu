from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import View
from . import forms


class LoginPageView(View):
    template_name = "authentication/login.html"
    form_class = forms.LoginForm

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
        form = self.form_class()
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
